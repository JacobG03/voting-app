import styles from './CreatePoll.module.css'
import { useState } from 'react'
import { useForm } from "react-hook-form";
import { getData, postData } from '../../services/api_calls';


function CreatePoll (props) {
  // * make a navbar shortcut to display this too
  // callback function Success to hide this component
  return (
    <div className={styles.main}>
      <div className={styles.top}>
        <img src={props.user.avatar} alt='User' />
        <span>{props.user.username}</span>
      </div>
      <CreatePollForm displayPoll={props.displayPoll} />
    </div>
  )
}

function CreatePollForm (props) {
  const { register, handleSubmit } = useForm();
  const onSubmit = data => {
    console.log(data)
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
      <div className={styles.fields}>
        <span>Topic:</span>
        <input placeholder='Topic' {...register("topic", {required: true})} />
      </div>
      <Options register={register}/>
      
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
    console.log('here')
    setOptions(prev => [...prev, {
      'id': options.length
    }])
  }

  return (
    <div className={styles.options}>
      {options.map(option => <Option options={options} setOptions={setOptions} option={option} key={option.id} register={props.register}/>)}
      <span onClick={() => addOption()}>Add Option</span>
    </div>
  )
}

function Option(props) {
  const removeOption = () => {
    var filtered = props.options.filter(function(option) { return option !== props.option; }); 
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