import AsyncStorage from "@react-native-async-storage/async-storage";
import { useContext } from "react";
import { View } from "react-native";
import { Button, Text } from "react-native-paper";
import { MyDispatchContext, MyUserContext } from "../../configs/MyUserContext";
import MyStyles from "../../styles/MyStyles";

const UserProfile = () => {
    const user = useContext(MyUserContext);
    const dispatch = useContext(MyDispatchContext);

    const logout = async () => {
        await AsyncStorage.removeItem("token");
        dispatch({
            "type": "logout"
        })
    }

    return (
        <View style={MyStyles.container}>
            <Text style={MyStyles.subject}>Chào {user?.username}</Text>
            <Button mode="contained-tonal" onPress={logout}>Đăng xuất</Button>
        </View>
    );
}

export default UserProfile;