import { ActivityIndicator, FlatList, Image, RefreshControl, ScrollView, Text, TouchableOpacity, View } from "react-native";
import { useState, useEffect } from "react";
import Styles from "../../styles/Styles";
import APIs, { endpoints } from "../../configs/APIs";
import { Chip, List, Searchbar } from "react-native-paper";
import { useNavigation } from "@react-navigation/native";
import Item from "./Item";

const Home = () => {
    const [categories, setCategories] = useState([]);
    const [courses, setCourses] = useState([]);
    const [loading, setLoading] = useState(false);
    const [cateId, setCateId] = useState("");
    const [q, setQ] = useState("");
    const [page, setPage] = useState(1);
    const nav = useNavigation();

    const loadCates = async () => {
        let res = await APIs.get(endpoints['categories']);
        setCategories(res.data);
    }

    const loadCourses = async () => {
        if (page > 0) {
            
            setLoading(true) 
            try {
                let url = `${endpoints['courses']}?page=${page}`;

                if (cateId || q )
                    url = `${url}&category_id=${cateId}&q=${q}`;

                let res = await APIs.get(url);
                if (page > 1)
                    setCourses(current => [...current, ...res.data.results]);
                else
                    setCourses(res.data.results);


                if (res.data.next === null)
                    setPage(0);
            } catch (ex) {
                console.error(ex);
            } finally {
                setLoading(false);
            }
        }
    }

    useEffect(() => {
        loadCates();
    }, []);

    useEffect(() => {
        let timer = setTimeout(() => loadCourses(), 500);
        
        return () => clearTimeout(timer);
    }, [cateId, q, page]);

    const loadMore = () => {
        if (page > 0 && !loading)
            setPage(page + 1);
    }

    const search = (value, callback) => {
        setPage(1);
        callback(value);
    }

    const refresh = () => {
        setPage(1);
        loadCourses();
    }


    return (
        <View style={Styles.container}>
            
            <View style={[Styles.row, Styles.wrap]}>
                <TouchableOpacity onPress={() => search(null, setCateId)}>
                    <Chip icon="label" style={Styles.margin}>Tất cả</Chip>
                </TouchableOpacity>

                {categories.map(c => <TouchableOpacity key={c.id} onPress={() => search(c.id, setCateId)}>
                    <Chip icon="label" style={Styles.margin}>{c.name}</Chip>
                </TouchableOpacity>)}
            </View>
            <Searchbar placeholder="Tìm khóa học..." value={q} onChangeText={t => search(t, setQ)} />
            {loading && <ActivityIndicator />}

            <FlatList refreshControl={<RefreshControl refreshing={loading} onRefresh={refresh} />} onEndReached={loadMore} data={courses} 
                    renderItem={({item}) => <Item item={item} routeName="lesson" params={{'courseId': item.id}} />} />

        </View>
    );
}
export default Home;