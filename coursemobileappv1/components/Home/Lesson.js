import { ActivityIndicator, FlatList, Image, Text, TouchableOpacity, View } from "react-native";
import Styles from "../../styles/Styles";
import { useState, useEffect } from "react";
import APIs, { endpoints } from "../../configs/APIs";
import { List } from "react-native-paper";
import Item from "./Item";

const Lesson = ({route}) => {
    const [lessons, setLessons] = useState([]);
    const [loading, setLoading] = useState(false);
    const courseId = route.params?.courseId;

    const loadLessons = async () => {
        try {
            setLoading(true);
            let res = await APIs.get(endpoints['lessons'](courseId));
            setLessons(res.data);
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        loadLessons();
    }, [courseId]);

    return (
        <View style={Styles.container}>
            {loading && <ActivityIndicator />}

            <FlatList data={lessons} renderItem={({item}) =>  <Item item={item} routeName="lessonDetails" params={{"lessonId": item.id}} />} />
        </View>
    );
}

export default Lesson;