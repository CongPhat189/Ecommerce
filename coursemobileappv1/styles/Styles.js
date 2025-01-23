import { StyleSheet } from "react-native";

export default StyleSheet.create({
    container: {
        flex: 1,
        padding: 5,
        // justifyContent: "center",
        // alignItems: "center"
    }, row: {
        flexDirection: "row"
    }, wrap: {
        flexWrap: "wrap"
    }, subject: {
        fontSize: 20,
        fontWeight: "bold",
        color: "blue"
    }, margin: {
        margin: 5
    }, box: {
        width: 80,
        height: 80,
        borderRadius: 10
    }
});