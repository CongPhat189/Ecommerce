import { ActivityIndicator, ScrollView, Text, View } from "react-native";
import { useEffect, useState } from "react/cjs/react.production.min";
import APIs, { endpoints } from "../../configs/APIs";
import MyStyles from "../../styles/MyStyles";
import React from 'react'
import Items from "./Items";

const Lessons = ({ route }) => {
    const courseId = route.params?.courseId;
    const [lessons, setLessons] = React.useState(null);

    const loadLessons = async () => {
        let res = await APIs.get(endpoints['lessons'](courseId));
        setLessons(res.data);
    }

    React.useEffect(() => {
        loadLessons();
    }, [courseId]);

    return (
        <ScrollView>
            {lessons===null?<ActivityIndicator />:<>
                {lessons.map(le => <Items key={le.id} item={le} routeName='lessonDetails' params={{'lessonId': le.id}} />)}
            </>}
        </ScrollView>
    );
}

export default Lessons;