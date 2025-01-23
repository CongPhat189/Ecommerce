import { List } from "react-native-paper";
import { TouchableOpacity, Image } from "react-native";
import MyStyles from "../../styles/MyStyles";
import { useNavigation } from "@react-navigation/native";

const Items = ({ item, routeName, params }) => {
    const nav = useNavigation();

    return <List.Item title={item.subject} description={item.created_date} 
                      left={() => <TouchableOpacity onPress={() => nav.navigate(routeName, params)}><Image source={{uri: item.image}} style={MyStyles.box} /></TouchableOpacity>} />
}

export default Items;