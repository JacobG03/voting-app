import styles from './Polls.module.css'
import {
  useEffect,
  useState,
  useCallback
} from 'react'
import { getData, postData } from '../../services/api_calls'


function Polls (props) {
  const [polls, setPolls] = useState(null)

  useEffect(() => {
    if (!props.user) {
      setPolls(null)
    }
  }, [props.user])

  useEffect(() => {
    getData('/polls')
    .then(data => {
      if (data.status === 200) {
        setPolls(data.body)
      }
    })
  }, [polls])

  if (!polls) {
    return null;
  }

  return (
    <div className={styles.polls}>
      {polls.map(poll => <Poll key={poll.id} data={poll} user={props.user}/>)}
    </div>
  )
}


function Poll (props) {
  const data = props.data;

  return (
    <div className={styles.poll}>
      <PollAuthor url={data.author_url} />
      <span className={styles.timestamp}>{data.timestamp}</span>
      <div className={styles.topic}>
        <span>{data.topic}</span>
      </div>
      <Options url={data.options_url} user={props.user}/>
    </div>
  )
}


function Options (props) {
  const [options, setOptions] = useState(null)

  useEffect(() => {
    getData(props.url)
    .then(data => setOptions(data.body))
  }, [props.url])

  const reqPoll = useCallback(() => {
    getData(props.url)
    .then(data => {
      setOptions(null) // to force rerender components
      setOptions(data.body)
    })
  }, [props.url])

  if (!options) {
    return null;
  }

  return (
    <div className={styles.options}>
      {options.map(option => 
      <Option 
        key={option.index} 
        data={option}
        reqPoll={reqPoll}
        user={props.user}
      />)}
    </div>
  )
}


function Option (props) {
  const [votes, setVotes] = useState(null)
  const [voted, setVoted] = useState(false)
  const data = props.data;
  // Depending on votes request status return 
  // either ability to vote or votes
  useEffect(() => {
    if (props.user) {
      getData(data.votes_url)
      .then(data => {
        if (data.status === 202) {
          // let user vote
          setVotes(true)
        } else if (data.status === 200) {
          // display votes
          setVotes(data.body.votes)
          setVoted(data.body.voted)
        }
      })
    }
  }, [props.user, data.votes_url])


  // if user anonymous
  if (votes === null) {
    return (
      <div className={styles.option}>
        <span>{data.body}</span>
      </div>
    )
  }
  // if user hasnt voted yet
  if (votes === true) {
    return <AllowVote data={data} reqPoll={props.reqPoll}/>
  }
  // show votes
  return <ShowVotes votes={votes} voted={voted}/>
}


// displays users avatars that voted
function ShowVotes (props) {
  
  return (
    <div className={`${styles.option} ${props.voted ? styles.voted : null}`}>
      <span>showing votes</span>
    </div>
  )
}


function AllowVote (props) {
  const data = props.data;
  const form = {'anonymous': false}

  const vote = () => {
    postData(data.votes_url, form)
    .then(obj => console.log(obj.body.msg))
    // refresh poll
    props.reqPoll()
  }

  return (
    <div 
      className={`${styles.option} ${styles.vote}`}
      onClick={() => vote()}
    >
      <span>{data.body}</span>
    </div>
  )
}


function PollAuthor (props) {
  const [author, setAuthor] = useState(null)

  useEffect(() => {
    getData(props.url)
    .then(data => {
      if (data.status === 200) {
        setAuthor(data.body)
      }
    })
  }, [props.url])

  if (!author) {
    return null;
  }

  return (
    <div className={styles.author}>
      <img src={author.avatar} alt='Avatar' />
      <span>{author.username}</span>
    </div>
  )
}




export default Polls;