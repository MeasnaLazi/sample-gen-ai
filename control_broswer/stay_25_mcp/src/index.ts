import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
    CallToolRequestSchema,
    ErrorCode,
    ListToolsRequestSchema,
    McpError,
    Tool,
} from "@modelcontextprotocol/sdk/types.js";

// const ADD_TWO_NUMBERS: Tool = {
//     name: "add_two_numbers",
//     description: "Calculate the sum of two numbers",
//     inputSchema: {
//         type: "object",
//         properties: {
//             a: {
//                 type: "number",
//                 description: "First number to add"
//             },
//             b: {
//                 type: "number",
//                 description: "Second number to add"
//             },
//         },
//         required: ["a", "b"],
//     }
// };

const STAY_25_SEARCH_TOOL: Tool = {
    name: "stay_25_search",
    description: "Search for Stay25 listings with various filters and pagination. Provide direct links to the user.",
    inputSchema: {
        type: "object",
        properties: {
            province: {
                type: "string",
                description: "The name of the province to search in"
            },
            check_in: {
                type: "string",
                description: "Check-in date (YYYY-MM-DD)"
            },
            check_out: {
                type: "string",
                description: "Check-out date (YYYY-MM-DD)"
            },
            guest: {
                type: "number",
                description: "Number of guests"
            },
            min_price: {
                type: "number",
                description: "Price range from"
            },
            max_price: {
                type: "number",
                description: "Price range to"
            },
            
        },
        required: ["province", "check_in", "check_out"],
    }
};

const STAY_25_LISTING_DETAILS_TOOL: Tool = {
    name: "stay_25_listing_details",
    description: "Get detailed information about a specific Stay25 listing. Provide direct links to the user.",
    inputSchema: {
        type: "object",
        properties: {
            listing_id: {
                type: "number",
                description: "The id of the listing."
            },
            check_in: {
                type: "string",
                description: "Check-in date (YYYY-MM-DD)"
            },
            check_out: {
                type: "string",
                description: "Check-out date (YYYY-MM-DD)"
            },
        },
        required: ["listing_id"],
    }
};

const ALL_TOOLS = [
    // ADD_TWO_NUMBERS,
    STAY_25_SEARCH_TOOL,
    STAY_25_LISTING_DETAILS_TOOL
] as const;

function addTwoNumbers(params: any) {
    const { a, b } = params;
    const result = a + b;
    return  {
        content: [{
            type: "text",
            text: result.toString()
        }],
        isError: false
    };
}

const BASE_URL = "https://platform.dev2.spacianet.com";

async function getProviceId(province: string) {
    const provinceUrl = `${BASE_URL}/api/cambodia/provinces`;
    const provinceLowwer = province.toLowerCase();
    try {
        const response = await fetch(provinceUrl);
        const responseJson = await response.json();
        const provices = responseJson["provinces"]
        const province = provices.find((item: any) => {
            return item.name.toLowerCase() === provinceLowwer;
        });
        return province ? province.id : "20"; // default to siem reap
    } catch (error) {
        console.error("Error fetching province data:", error);
        return "20"; //siem reap
    }
}

async function stay25Search(params: any) {
    const { province, check_in, check_out, guest = 1, min_price = 20, max_price =1000 } = params;
    const searchUrl = new URL(`${BASE_URL}/json/v2/guest/search`);
    const provinceId = await getProviceId(province);

    if (province) searchUrl.searchParams.append("province", provinceId);
    if (check_in) searchUrl.searchParams.append("check_in", check_in);
    if (check_out) searchUrl.searchParams.append("check_out", check_out);
    if (guest) searchUrl.searchParams.append("guest", guest.toString());
    if (min_price) searchUrl.searchParams.append("min_price", min_price.toString());
    if (max_price) searchUrl.searchParams.append("max_price", max_price.toString());

    searchUrl.searchParams.append("offset", "0");
    searchUrl.searchParams.append("limit", "22");

    try {
        const response = await fetch(searchUrl.toString())
        const responseJson = await response.json();
        const data = responseJson.data;
        const result = data.map((item: any) => {
            item["url"] = `${BASE_URL}/listing-details/${item.id}?check-in=${check_in}&check-out=${check_out}&guest=${guest}&source=0`;
            return item;
        })

        return {
            content: [{
                type: "text",
                text: JSON.stringify({
                    searchUrl: searchUrl.toString(),
                    ...result
                }, null, 2)
            }],
            isError: false
          };
    } catch (error) {
        return {
            content: [{
              type: "text",
              text: JSON.stringify({
                error: error instanceof Error ? error.message : String(error),
                searchUrl: searchUrl.toString()
              }, null, 2)
            }],
            isError: true
          };
    }
}

async function stay25Detail(params: any) {
    const { listing_id, check_in, check_out } = params;
    const searchUrl = new URL(`${BASE_URL}/json/v2/guest/listing_detail/${listing_id}`);

    if (check_in) searchUrl.searchParams.append("check_in", check_in);
    if (check_out) searchUrl.searchParams.append("check_out", check_out);

    try {
        const response = await fetch(searchUrl.toString())
        const responseJson = await response.json();
        const result = responseJson.data;

        return {
            content: [{
                type: "text",
                text: JSON.stringify({
                    searchUrl: searchUrl.toString(),
                    result
                }, null, 2)
            }],
            isError: false
          };
    } catch (error) {
        return {
            content: [{
              type: "text",
              text: JSON.stringify({
                error: error instanceof Error ? error.message : String(error),
                searchUrl: searchUrl.toString()
              }, null, 2)
            }],
            isError: true
          };
    }
}

const server = new Server({ 
    name: "stay_25", 
    version: "1.0.0" }, {
        capabilities: {
            tools: {}
        }
    });

server.setRequestHandler(ListToolsRequestSchema, async () => ({
    tools: ALL_TOOLS,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
    try {
  
        switch (request.params.name) {
            // case "add_two_numbers": {
            //     return addTwoNumbers(request.params.arguments);
            // }
            case "stay_25_search": {
                return stay25Search(request.params.arguments);
            }
            case "stay_25_listing_details": {
                return stay25Detail(request.params.arguments);
            }
    
            default:
                throw new McpError(
                    ErrorCode.MethodNotFound,
                    `Unknown tool: ${request.params.name}`
                );
        }
    } catch (error) {
        return {
            content: [{
                type: "text",
                text: `Error: ${error instanceof Error ? error.message : String(error)}`
            }],
            isError: true
        };
    }
});

async function runServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error("Stay25 MCP Server running on stdio");
}
  
runServer().catch((error) => {
    console.error("Fatal error running server:", error);
    process.exit(1);
});