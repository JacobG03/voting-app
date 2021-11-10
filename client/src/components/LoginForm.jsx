import styles from './LoginForm.module.css'
import { useState } from 'react'
import { useForm } from "react-hook-form";
import { getData, postData } from '../services/api_calls';


function Form (props) {
  const [form, changeForm] = useState(false)

  if (!form) {
    return <LoginForm 
      setUser={props.setUser} 
      displayForm={props.displayForm}
      changeForm={changeForm}
    />
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
      <div>
        <span>Email:</span>
        <input placeholder='Email' {...register("email", {required: true})} />
        {errors.email && <span>This field is required</span>}
        <span>Password:</span>
        <input placeholder='Password' type='password' {...register("password", { required: true })} />
        {errors.password && <span>This field is required</span>}
      </div>
      
      <input type="submit" className={styles.submit} value='Sign In'/>
      <span 
        className={styles.switch}
        onClick={() => props.changeForm(last => !last)}
      >
        Register
      </span>
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
      <div>
        <span>Username:</span>
        <input placeholder='Username' {...register("username", {required: true, minLength: 3, maxLength: 64})} />
        <span>Email:</span>
        <input placeholder='Email' {...register("email", {required: true, minLength: 1, maxLength: 128})} />
        <span>Password:</span>
        <input placeholder='Password' type='password' {...register("password", { required: true , minLength: 3, maxLength: 256})} />
        {errors.password && <span>This field is required</span>}
        <span>Repeat Password:</span>
        <input placeholder='Repeat Password' type='password' {...register("password2", { required: true , minLength: 3, maxLength: 256})} />
        <span>Avatar:</span>
        <input placeholder='URL: [PNG, JPG, GIF]' {...register("avatar", { required: true })} />
      </div>
      <input type="submit" className={styles.submit} value='Sign Up'/>
      <span className={styles.switch} onClick={() => props.changeForm(last => !last)}>Login</span>
    </form>
  );
}

export default Form;