import { List } from "react-native-paper";
import { TouchableOpacity, Image } from "react-native";
import Styles from "../../styles/Styles";
import { useNavigation } from "@react-navigation/native";
import moment from "moment";

const Item = ({item, routeName, params}) => {
    const nav = useNavigation();

    return <List.Item key={item.id} title={item.subject}  description={item.created_date && moment(item.created_date).fromNow()}
                        left={props => <TouchableOpacity onPress={() => nav.navigate(routeName, params)}>
                                    <Image source={{uri: item.image}} style={Styles.box} /></TouchableOpacity>} />;
}

export default Item;