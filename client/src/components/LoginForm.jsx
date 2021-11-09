import styles from './LoginForm.module.css'
import { useState } from 'react'
import { useForm } from "react-hook-form";
import { getData, postData } from '../services/api_calls';


function Form (props) {
  const [form, changeForm] = useState(false)

  if (!form) {
    return <LoginForm setUser={props.setUser} displayForm={props.displayForm}/>
  }
  return <RegisterForm changeForm={changeForm} />
}


function LoginForm (props) {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const onSubmit = data => {
    postData('/login', data)
    .then(obj => {
      if (obj.status === 200) {
        getData('/user')
        .then(obj => {
          if(obj.status === 200) {
            props.setUser(obj.body)
            props.displayForm(false)
          }
        })
      }
    })
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
      <input {...register("email", {required: true})} />
      
      <input type='password' {...register("password", { required: true })} />
      {errors.exampleRequired && <span>This field is required</span>}
      
      <input type="submit" />
    </form>
  );
}

function RegisterForm (props) {
  const { register, handleSubmit, formState: { errors } } = useForm();
  const onSubmit = data => {
    postData('/register', data)
    .then(obj => {
      if (obj.status === 200) {
        console.log(obj.body)
        props.changeForm(form => !form)
      } else {
        console.log(obj.body)
      }
    })
  };

  return (
    <form className={styles.form} onSubmit={handleSubmit(onSubmit)}>
      <input {...register("username", {required: true, minLength: 3, maxLength: 64})} />
      <input {...register("email", {required: true, minLength: 1, maxLength: 128})} />
      
      <input type='password' {...register("password", { required: true , minLength: 3, maxLength: 256})} />
      {errors.password && <span>This field is required</span>}
      <input type='password' {...register("password2", { required: true , minLength: 3, maxLength: 256})} />
      
      <input type="submit" />
    </form>
  );
}

export default Form;