import styles from  './App.module.css';
import {
  useEffect,
  useState
} from 'react';
import { getData } from './services/api_calls';
import CreatePoll from './components/polls/CreatePoll';
import Polls from './components/polls/Polls';
import Form from './components/LoginForm';
import Navbar from './components/Navbar';


function App() {
  const [user, setUser] = useState(null)
  const [form, displayForm] = useState(false)

  // Get user object if user is logged in else null
  useEffect(() => {
    getData('/user')
    .then(obj => {
      if(obj.status === 200) {
        setUser(obj.body)
      } else {
        console.log('User is anonymous')
      }
    })
  }, [])

  return (
    <div className={styles.App}>
      <Navbar user={user} setUser={setUser} displayForm={displayForm}/>
      <div className={styles.content}>
        {form ? <Form setUser={setUser} displayForm={displayForm}/>: null}
        {user ? <CreatePoll />: null}
        <Polls user={user}/>
      </div>
    </div>
  );
}

export default App;
