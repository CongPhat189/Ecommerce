import AsyncStorage from "@react-native-async-storage/async-storage";
import { useNavigation } from "@react-navigation/native";
import { useContext, useState } from "react";
import { View } from "react-native"
import { Button, Icon, TextInput } from "react-native-paper";
import APIs, { authApis, endpoints } from "../../configs/APIs";
import { MyDispatchContext } from "../../configs/MyUserContext";
import MyStyles from "../../styles/MyStyles"

const Login = () => {
    const [user, setUser] = useState({});
    const [loading, setLoading] = useState(false);
    const dispatch = useContext(MyDispatchContext);
    const nav = useNavigation();

    const users = {
        "username": {
            "title": "Tên đăng nhập",
            "field": "username",
            "icon": "text",
            "secureTextEntry": false
        }, "password": {
            "title": "Mật khẩu",
            "field": "password",
            "icon": "eye",
            "secureTextEntry": true
        }
    }

    const change = (value, field) => {
        setUser({...user, [field]: value});
    }

    const login = async () => {
        setLoading(true);
        try {
            let res = await APIs.post(endpoints['login'], {
                ...user,
                'grant_type': 'password',
                'client_id': 'Vbe8euZZQJoWJ2UzW9wDThg4hJEZHHbhFmnfj7UR',
                'client_secret': 'cVm4w4hSdy4MtwbP4KuNgXkGPeQJ9yrQdBvXHGR6b3e97F2bYqQ81XJ49FEufzjcw4SKwpuOZQiCLsNelHY1MkuYTGBRcSqtWmSlebSUk27WfyDskCB2VeCQihnEKdZ2' 
            });
            console.info(res.data);
            await AsyncStorage.setItem('token', res.data.access_token);

            setTimeout(async () => {
                let user = await authApis(res.data.access_token).get(endpoints['current-user']);
                console.info(user.data);

                dispatch({
                    "type": "login",
                    "payload": user.data
                });

                nav.navigate("home");

            }, 100);

        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    }

    return (
        <View>
            {Object.values(users).map(u => <TextInput secureTextEntry={u.secureTextEntry} key={u.field} value={user[u.field]} onChangeText={t => change(t, u.field)} 
            style={MyStyles.margin} placeholder={u.title} right={<TextInput.Icon icon={u.icon} />} />)}
            <Button loading={loading} mode="contained" onPress={login}>ĐĂNG NHẬP</Button>
        </View>
    );
}

export default Login;