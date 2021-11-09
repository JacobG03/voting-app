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
        <span>{'<Voting App>'}</span>
        <button 
          className={styles.signin}
          onClick={() => props.displayForm(form => !form)}
        >
          Sign in
        </button>
      </nav>
    )
  }

  return (
    <nav className={styles.navbar}>
      <span>{'<Voting App>'}</span>
      <button 
        className={styles.signin}
        onClick={() => signout()}
      >
        Sign out
      </button>
    </nav>
  )
}

export default Navbar;