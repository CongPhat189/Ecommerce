
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Home from './components/Home/Home';
import LessonDetails from './components/Home/LessonDetails';
import Lessons from './components/Home/Lessons';
import 'moment/locale/vi';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Login from './components/User/Login';
import Register from './components/User/Register';
import { Icon } from 'react-native-paper';
import { MyDispatchContext, MyUserContext } from './configs/MyUserContext';
import { useContext, useReducer } from 'react';
import MyUserReducers from './configs/MyUserReducers';
import UserProfile from './components/User/Profile';

const Stack = createNativeStackNavigator();

const StackNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{headerShown: false}}>
      <Stack.Screen name="index" component={Home} />
      <Stack.Screen name="lessons" component={Lessons} />
      <Stack.Screen name="lessonDetails" component={LessonDetails} />
    </Stack.Navigator>
  );
}

const Tab = createBottomTabNavigator();
const TabNavigator = () => {
  const user = useContext(MyUserContext);

  return (
    <Tab.Navigator>
      <Tab.Screen name="home" component={StackNavigator} options={{title: "Màn hình chính", tabBarIcon: () => <Icon source="home-account" size={20} />}} />
      {user===null?<>
        <Tab.Screen name="login" component={Login} options={{title: "Đăng nhập", tabBarIcon: () => <Icon source="account-check" size={20} />}} />
        <Tab.Screen name="register" component={Register} options={{title: "Đăng ký", tabBarIcon: () => <Icon source="account-plus" size={20} />}} />
      </>:<>
        <Tab.Screen name="profile" component={UserProfile} options={{title: "Tài khoản", tabBarIcon: () => <Icon source="account-check" size={20} />}} />
      </>}
    </Tab.Navigator>
  );
}

export default function App() {
  const [user, dispatch] = useReducer(MyUserReducers, null);

  return (
      <NavigationContainer>
        <MyUserContext.Provider value={user}>
          <MyDispatchContext.Provider value={dispatch}>
            <TabNavigator />
          </MyDispatchContext.Provider>
        </MyUserContext.Provider>
      </NavigationContainer>
  );
}
