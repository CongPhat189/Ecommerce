import { Image, KeyboardAvoidingView, Platform, ScrollView, Text, TouchableOpacity } from "react-native";
import { Button, TextInput } from "react-native-paper";
import Styles from "../../styles/Styles";
import * as ImagePicker from 'expo-image-picker';
import { useState } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { useNavigation } from "@react-navigation/native";

const Register = () => {
    const [user, setUser] = useState({
        "username": "",
        "password": ""
    });
    const [loading, setLoading] = useState(false);
    const users = {
        "first_name": {
            "title": "Tên",
            "field": "first_name",
            "secure": false,
            "icon": "text"
        },
        "last_name": {
            "title": "Họ và tên lót",
            "field": "last_name",
            "secure": false,
            "icon": "text"
        },
        "username": {
            "title": "Tên đăng nhập",
            "field": "username",
            "secure": false,
            "icon": "text"
        },  "password": {
            "title": "Mật khẩu",
            "field": "password",
            "secure": true,
            "icon": "eye"
        }, "confirm": {
            "title": "Xác nhận mật khẩu",
            "field": "confirm",
            "secure": true,
            "icon": "eye"
        }
    }
    const [avatar, setAvatar] = useState();

    const nav = useNavigation();

    const updateUser = (value, field) => {
        setUser({...user, [field]: value});
    }

    const pickImage = async () => {
        let { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
        if (status !== 'granted') {
            alert("Permissions denied!");
        } else {
            const result = await ImagePicker.launchImageLibraryAsync();
            if (!result.canceled)
                setAvatar(result.assets[0]);
        }
    }

    const register = async () => {
        
        setLoading(true);
        try {
            const form = new FormData();

            for (let k in user)
                if (k !== 'confirm')
                    form.append(field, user[k]);

            console.info(form);

            form.append('avatar', {
                uri: avatar.uri,
                name: avatar.fileName,
                type: avatar.type
            });

            
            await APIs.post(endpoints['register'], form, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });

            nav.navigate("login");
        } catch (ex) {

        } finally {
            setLoading(false);
        }
    }

    return (
        <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>
            <ScrollView>
                {Object.values(users).map(u => <TextInput right={<TextInput.Icon icon={u.icon} />} key={u.field} 
                        secureTextEntry={u.secure} style={Styles.margin} placeholder={u.title} 
                        value={user[u.field]}  onChangeText={t => updateUser(t, u.field)}  />)}

                <TouchableOpacity onPress={pickImage}>
                    <Text>Chọn ảnh đại diện</Text>
                </TouchableOpacity>

                {avatar ? <Image source={{ uri: avatar.uri }} style={{ width: 100, height: 100 }} /> : ""}

                <Button onPress={register} loading={loading} style={Styles.margin} 
                        icon="account-check" mode="contained">Đăng ký</Button>
            </ScrollView>
        </KeyboardAvoidingView>
    );
}

export default Register;