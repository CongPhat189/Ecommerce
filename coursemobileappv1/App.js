import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import Home from './components/Home/Home';
import Lesson from './components/Home/Lesson';
import LessonDetails from './components/Home/LessonDetails';
import 'moment/locale/vi';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import Register from './components/User/Register';
import Login from './components/User/Login';
import { Icon } from 'react-native-paper';
import { MyDispatchContext, MyUserContext } from './configs/UserContexts';
import { useContext, useReducer } from 'react';
import MyUserReducer from './configs/UserReducers';
import UserProfile from './components/User/UserProfile';

const Stack = createNativeStackNavigator();

const StackNavigator = () => {
    return (
      <Stack.Navigator screenOptions={{headerShown: false}}>
        <Stack.Screen name="home" component={Home} options={{'title': 'Màn hình chính'}} />
        <Stack.Screen name="lesson" component={Lesson} />
        <Stack.Screen name="lessonDetails" component={LessonDetails} />
      </Stack.Navigator>
    );
}

const Tab = createBottomTabNavigator();
const TabNavigator = () => {
  const user = useContext(MyUserContext);

  return (
    <Tab.Navigator>
      <Tab.Screen name="index" component={StackNavigator} options={{title: 'Màn hình chính', tabBarIcon: () => <Icon source="home-account" size={20} />}} />

      {user===null?<>
        <Tab.Screen name="register" component={Register} options={{title: 'Đăng ký', tabBarIcon: () => <Icon source="account" size={20} />}} />
        <Tab.Screen name="login" component={Login} options={{title: 'Đăng nhập', tabBarIcon: () => <Icon source="account-check" size={20} />}} />
      </>:<>
        <Tab.Screen name="profile" component={UserProfile} options={{title: 'Tài khoản', tabBarIcon: () => <Icon source="account" size={20} />}} />
      </>}

      
    </Tab.Navigator>
  );
}


export default function App() {
  const [user, dispatch] = useReducer(MyUserReducer, null);

  return (
    
        <NavigationContainer>
          <MyUserContext.Provider value={user}>
            <MyDispatchContext.Provider value={dispatch}>
              <TabNavigator />
            </MyDispatchContext.Provider>
          </MyUserContext.Provider>
        </NavigationContainer>
   
  )
}
