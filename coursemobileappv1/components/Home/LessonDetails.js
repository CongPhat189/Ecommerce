import { ActivityIndicator, ScrollView, Text } from "react-native";
import { useState, useEffect } from "react";
import Styles from "../../styles/Styles";
import APIs, { endpoints } from "../../configs/APIs";
import { Button, Card, Chip, List } from "react-native-paper";
import RenderHTML from "react-native-render-html";
import { View } from "react-native";
import { Image } from "react-native";
import moment from "moment";

const LessonDetails = ({route}) => {
    const lessonId = route.params?.lessonId;
    const [loading, setLoading] = useState(false);
    const [lesson, setLesson] = useState(null);
    const [comments, setComments] = useState(null);


    const loadLesson = async () => {
        try {
            setLoading(true);
            let res = await APIs.get(endpoints['lesson-details'](lessonId));
            setLesson(res.data);
        } catch (ex) {
            console.error(ex);
        } finally {
            setLoading(false);
        }
    }

    const loadComments = async () => {
        let res = await APIs.get(endpoints['comments'](lessonId));
        setComments(res.data);
        console.info(res.data);
    }

    useEffect(() => {
        loadLesson();
    }, [lessonId]);

    const scroll = ({nativeEvent}) => {
        if (isCloseToBottom(nativeEvent) && comments === null) {
            loadComments();
        }
    }

    const isCloseToBottom = ({layoutMeasurement, contentOffset, contentSize}) => {
        return layoutMeasurement.height + contentOffset.y >= contentSize.height - 20;
    }

    return (
        <ScrollView style={Styles.margin} onScroll={scroll}>
            {loading && <ActivityIndicator />}
            {lesson && 
                <Card>
                    <Card.Title titleStyle={Styles.subject} title={lesson.subject}  />
                    <Card.Cover source={{ uri: lesson.image }} />
                    
                    <Card.Content>
                        <View style={Styles.row}>
                            {lesson.tags.map(t => <Chip icon="label" key={t.id} style={Styles.margin}>{t.name}</Chip>)}
                        </View>
                        <RenderHTML source={{'html': lesson.content}} />
                    </Card.Content>
                </Card>}

            <View>
                {comments && comments.map(c => <List.Item key={c.id} title={c.content}
                                                          description={moment(c.created_date).fromNow()}
                                                          left={() => <Image source={{uri: c.user.image}} style={Styles.box} />}
                                                        />)}
            </View>
        </ScrollView>
    );
}

export default LessonDetails;