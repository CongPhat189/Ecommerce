import { useState } from "react";
import { Image, KeyboardAvoidingView, Platform, Text, Touchable, TouchableOpacity, View } from "react-native"
import { Button, TextInput, HelperText } from "react-native-paper";
import MyStyles from "../../styles/MyStyles"
import * as ImagePicker from 'expo-image-picker';
import APIs, { endpoints } from "../../configs/APIs";
import { useNavigation } from "@react-navigation/native";

const Register = () => {
    const [user, setUser] = useState({});

    const users = {
        "first_name": {
            "title": "Tên",
            "field": "first_name",
            "icon": "text",
            "secureTextEntry": false
        },
        "last_name": {
            "title": "Họ và tên lót",
            "field": "last_name",
            "icon": "text",
            "secureTextEntry": false
        },
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
        }, "confirm": {
            "title": "Xác nhận mật khẩu",
            "field": "confirm",
            "icon": "eye",
            "secureTextEntry": true
        }
    }
    const nav = useNavigation();
    const [loading, setLoading] = useState(false);
    const [err, setErr] = useState(false);

    const change = (value, field) => {
        setUser({...user, [field]: value});
    }

    const pickImage = async () => {
        let { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();

        if (status !== 'granted') {
            alert("Permissions denied!");
        } else {
            const result = await ImagePicker.launchImageLibraryAsync();
            if (!result.canceled)
                change(result.assets[0], 'avatar');
            }
        }

    const register = async () => {
        if (user.password !== user.confirm)
            setErr(true);
        else {
            setErr(false);
            let form = new FormData();

            for (let key in user)
                if (key !== 'confirm') {
                    if (key === 'avatar') {
                        form.append('avatar', {
                            uri: user.avatar.uri,
                            name: user.avatar.fileName,
                            type: user.avatar.type
                        })
                    } else
                        form.append(key, user[key]);
                }

            console.info(form)

                
            setLoading(true);
            try {
                let res = await APIs.post(endpoints['register'], form, {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                });
                console.info(res.data)
                nav.navigate("login");
            } catch (ex) {
                console.error(JSON.stringify(ex));
            } finally {
                setLoading(false);
            }
        }
    }
    
    return (
        <View style={MyStyles.container}>
            <KeyboardAvoidingView  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}>

                <HelperText type="error" visible={err}>
                Mật khẩu KHÔNG khớp
                </HelperText>
            
                {Object.values(users).map(u => <TextInput secureTextEntry={u.secureTextEntry} key={u.field} value={user[u.field]} onChangeText={t => change(t, u.field)} 
                style={MyStyles.margin} placeholder={u.title} right={<TextInput.Icon icon={u.icon} />} />)}

                <TouchableOpacity onPress={pickImage}>
                    <Text style={MyStyles.margin}>Chọn ảnh đại diện...</Text>
                </TouchableOpacity>

                {user.avatar ? <Image source={{ uri: user.avatar.uri }} style={{ width: 100, height: 100 }} /> : ""}

                <Button loading={loading} mode="contained" onPress={register}>ĐĂNG KÝ</Button>
            </KeyboardAvoidingView>
        </View>
    );
}

export default Register;