import { type RouteConfig, index, layout, route } from "@react-router/dev/routes";

export default [
    layout("layout/Layout.tsx", [
        index("routes/home.tsx"),
        route("recipe-search", "routes/recipe_search.tsx"),
    ])
] satisfies RouteConfig;
