import Keycloak from "keycloak-js"

const keycloak = new Keycloak({
    url: "http://localhost:8090/auth",
    realm: "example",
    clientId: "umm",
});


export default keycloak;
