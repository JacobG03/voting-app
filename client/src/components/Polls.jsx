import styles from './Poll.module.css'
import {
  useEffect,
  useState,
  useCallback
} from 'react'
import { getData, postData } from '../services/api_calls'


function Polls (props) {
  const [polls, setPolls] = useState(null)

  useEffect(() => {
    getData('/polls')
    .then(data => {
      if (data.status === 200) {
        setPolls(data.body)
      }
    })
  }, [])

  if (!polls) {
    return null;
  }

  return (
    <div className={styles.polls}>
      {polls.map(poll => <Poll key={poll.id} data={poll} />)}
    </div>
  )
}


function Poll (props) {
  const [data, setData] = useState(props.data)

  // refresh poll callback
  console.log(props.data)

  if (!data) {
    return null;
  }

  return (
    <div className={styles.poll}>
      <PollAuthor url={data.author_url} />
      <span className={styles.timestamp}>{data.timestamp}</span>
      <div className={styles.topic}>
        <span>{data.topic}</span>
      </div>
      <Options url={data.options_url}/>
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
    getData(data.votes_url)
    .then(data => {
      if (data.status === 403) {
        // let user vote
        setVotes(true)
      } else if (data.status === 200) {
        // display votes
        setVotes(data.body.votes)
        setVoted(data.body.voted)
      }
    })
  }, [data.votes_url])


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
    return <OptionVote data={data} reqPoll={props.reqPoll}/>
  }
  // show votes
  return <OptionVotes votes={votes} voted={voted}/>
}


function OptionVotes (props) {
  const votes = props.votes;
  console.log(votes)
  return (
    <div className={`${styles.option} ${props.voted ? styles.voted : null}`}>
      <span>showing votes</span>
    </div>
  )
}


function OptionVote (props) {
  const data = props.data;
  const form = {'anonymous': false}

  const vote = () => {
    postData(data.votes_url, form)
    .then(data => console.log(data))
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