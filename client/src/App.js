import styles from  './App.module.css';
import {
  useEffect,
  useState
} from 'react';
import { getData } from './services/api_calls';
import CreatePoll from './components/CreatePoll';
import Polls from './components/Polls';


function App() {
  const [user, setUser] = useState(null)

  // Get user object if user is logged in else null
  useEffect(() => {
    getData('/user')
    .then(obj => {
      if(obj.status === 200) {
        setUser(obj.body)
      }
    })
  }, [])
  
  return (
    <div className={styles.App}>
      {user ? <CreatePoll /> : null}
      <Polls />
    </div>
  );
}

export default App;
