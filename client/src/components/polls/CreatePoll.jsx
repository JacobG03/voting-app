import styles from './CreatePoll.module.css'
import { useState } from 'react'
import { useForm } from "react-hook-form";
import { postData } from '../../services/api_calls';


function CreatePoll (props) {
  // * make a navbar shortcut to display this too
  // callback function Success to hide this component
  return (
    <div className={styles.main}>
      <div className={styles.top}>
        <img src={props.user.avatar} alt='User' />
        <span>{props.user.username}</span>
      </div>
      <CreatePollForm rerenderPolls={props.rerenderPolls} displayPoll={props.displayPoll} />
    </div>
  )
}

function CreatePollForm (props) {
  const { register, handleSubmit, unregister } = useForm();
  const onSubmit = data => {
    var new_data = {
      'topic': data.topic,
      'options': []
    }

    for (const key in data) {
      if (key !== 'topic') {
        new_data['options'].push(data[key])
      }
    }

    postData('/polls', new_data)
    .then(data => {
      if (data.status === 200) {
        props.rerenderPolls(prev => !prev)
        props.displayPoll(false)
      } else {
        console.log(data.body)
      }
    })
  }


  return (
    <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
      <div className={styles.fields}>
        <span>Topic:</span>
        <input placeholder='Topic' {...register("topic", {required: true})} />
      </div>
      <Options unregister={unregister} register={register}/>
      
      <div className={styles.finish}>
        <span onClick={() => props.displayPoll(prev => !prev)}>Cancel</span>
        <input type="submit" className={styles.submit} value='Create Poll'/>
      </div>
    </form>
  );
}

function Options(props) {
  const [options, setOptions] = useState([])

  const addOption = () => {
    setOptions(prev => [...prev, {
      'id': options.length
    }])
  }

  return (
    <div className={styles.options}>
      {options.map(option => <Option unregister={props.unregister} options={options} setOptions={setOptions} option={option} key={option.id} register={props.register}/>)}
      <span onClick={() => addOption()}>Add Option</span>
    </div>
  )
}

function Option(props) {
  const removeOption = () => {
    var filtered = props.options.filter(function(option) { return option !== props.option; }); 
    props.unregister(`option-${props.option.id}`)
    props.setOptions(filtered)
  }

  return (
    <div className={styles.option}>
      <input placeholder={`Option ${props.option.id}`} {...props.register(`option-${props.option.id}`, { required: true })} />
      <span onClick={() => removeOption()}>-</span>
    </div>
  )
}

export default CreatePoll;