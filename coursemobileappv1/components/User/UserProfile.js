import AsyncStorage from "@react-native-async-storage/async-storage";
import { useNavigation } from "@react-navigation/native";
import { useContext } from "react";
import { Text } from "react-native";
import { Button } from "react-native-paper";
import { MyDispatchContext, MyUserContext } from "../../configs/UserContexts";
import Styles from "../../styles/Styles";

const UserProfile = () => {
    const user = useContext(MyUserContext);
    const dispatch = useContext(MyDispatchContext)
    const nav = useNavigation();

    console.info("===");
    console.info(user);

    const logout = async () => {
        await AsyncStorage.removeItem('token');

        dispatch({"type": "logout"});
        
        nav.navigate("index");
    }

    return (
        <>
            <Text style={Styles.subject}>Chào {user.username}</Text>
            <Button onPress={logout} style={Styles.margin} mode="outlined">Đăng xuất</Button>
        </>
    );
}

export default UserProfile;