import styles from './Navbar.module.css'
import { useCallback } from 'react'
import { getData } from '../services/api_calls'


function Navbar(props) {

  const signout = useCallback(() => {
    getData('/logout')
    .then(obj => {
      if (obj.status === 200) {
        props.setUser(false)
      }
    })
  }, [props])
  
  if (!props.user) {
    return (
      <nav className={styles.navbar}>
        <div className={styles.content}>
          <span>{'<Voting App>'}</span>
          <button 
            className={styles.signin}
            onClick={() => props.displayForm(form => !form)}
          >
            Sign in
          </button>
        </div>
      </nav>
    )
  }

  return (
    <nav className={styles.navbar}>
      <div className={styles.content}>
        <span>{'<Voting App>'}</span>
        <div className={styles.action}>
          {props.user ? <button 
            className={styles.signin}
            onClick={() => props.displayPoll(prev => !prev)}
          >
            Create Poll
          </button>: null}
          <button 
            className={styles.signin}
            onClick={() => signout()}
          >
            Sign out
          </button>
        </div>
      </div>
    </nav>
  )
}

export default Navbar;