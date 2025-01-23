import React from "react";
import { ActivityIndicator, Image, ScrollView, Text, View } from "react-native";
import { Card, List } from "react-native-paper";
import RenderHTML from "react-native-render-html";
import APIs, { endpoints } from "../../configs/APIs";
import MyStyles from "../../styles/MyStyles";
import moment from "moment";

const LessonDetails = ({route}) => {
    const lessonId = route.params?.lessonId;
    const [lesson, setLesson] = React.useState(null);
    const [comments, setComments] = React.useState(null);

    const loadLesson = async () => {
        let res = await APIs.get(endpoints['lesson-details'](lessonId));
        setLesson(res.data);
    }

    const loadComments = async () => {
        let res = await APIs.get(endpoints['comments'](lessonId));
        setComments(res.data);

        console.info(res.data)
    }

    React.useEffect(() => {
        loadLesson();
    }, [lessonId]);

    const isCloseToBottom = ({layoutMeasurement, contentOffset, contentSize}) => {
        return layoutMeasurement.height + contentOffset.y >= contentSize.height - 20;
    }

    const reachBottom = ({nativeEvent}) => {
        if (isCloseToBottom(nativeEvent) && comments === null)
            loadComments();
    }

    return (
        <ScrollView onScroll={reachBottom}>
            {lesson===null?<ActivityIndicator />:<>
                <Card>
                   
                    <Card.Cover source={{ uri: lesson.image }} />
                    <Card.Content>
                        <Text variant="titleLarge" style={MyStyles.subject}>{lesson.subject}</Text>
                    
                        <RenderHTML source={{'html': lesson.content}} />
                    </Card.Content>
                    
                    
                </Card>
            </>}

            <View>
                {comments===null?<ActivityIndicator />:<>
                
                    {comments.map(c => <List.Item title={c.content} description={moment(c.created_date).fromNow()}  
           left={() => <Image style={MyStyles.box} source={{uri: c.user.image}} />} /> )}

                </>}
            </View>
        </ScrollView>
    );
}

export default LessonDetails;