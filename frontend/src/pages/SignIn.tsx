"use client"

import { useState } from "react"
import { LogIn, Mail, Lock } from "lucide-react"
import { doSignInUserWithEmailAndPassword, signInWithGoogle } from "../firebase/auth";
import { signInApi } from "../api/signInApi";
import { useNavigate } from "react-router-dom";
import { UserCredential } from "firebase/auth";
import { useDispatch } from 'react-redux';
import { setUserEmail, setUserMFA } from "../features/userSlice";
import { z } from 'zod'
import { toast } from "react-toastify";
export default function SignInPage() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const [ isSigningIn, setIsSigningIn ] = useState(false)
  const dispatch = useDispatch();

  const navigate = useNavigate();

  const onGoogleSignIn = async (_e: React.MouseEvent<HTMLDivElement>) => {
    // e.preventDefault();
    if(!isSigningIn){
        setIsSigningIn(true);
        const userCredential: UserCredential = await signInWithGoogle();
        const idToken = await userCredential.user.getIdToken();
        const response = await signInApi(idToken);
        
        
        if (response?.data?.requireRegistration) {
          navigate('/signup');
        }else{
          console.log("response?.data?.user?.email", response?.data?.user?.email)
          dispatch(setUserEmail(response?.data?.user?.email));
          dispatch(setUserMFA(response?.data?.user?.mfaEnabled));

        console.log('response?.data?.mfaEnabled', response?.data?.mfaEnabled)
        if(response?.data?.mfaEnabled){
          navigate('/mfa')
        }else{
          navigate('/dashboard')
        }
      }
    }
  }

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    try {
      event.preventDefault();
  
      // Define the schema for validation
      const schema = z.object({
        email: z.string().email("Invalid email address"),
        password: z.string().min(6, "Password must be at least 8 characters long"),
      });
  
      // Validate the input data
      const parsedInput = schema.safeParse({ email, password });
      
      if (!parsedInput.success) {
        console.log('parsedInput.error', parsedInput.error)
        // Handle validation errors
        toast.warn("Invalid Email/password");
        return; // Stop further execution if validation fails
      }
  
      setIsSigningIn(true);
  
      // Proceed with Firebase authentication
      const userCredential = await doSignInUserWithEmailAndPassword(email, password);
      console.log('userCredential', userCredential)
      const idToken = await userCredential.user.getIdToken();
  
      if (!idToken) {
        throw new Error('Failed to get authentication token');
      }
  
      // Call the sign-in API
      const response = await signInApi(idToken);
  
      if (response?.data?.requireRegistration) {
        navigate('/signup');
      } else {
        dispatch(setUserEmail(response?.data?.user?.email));
        console.log('response?.data?.user?.isMFAEnabled', response?.data?.user?.mfaEnabled)
        dispatch(setUserMFA(response?.data?.user?.mfaEnabled));
        toast.success("Signin Successful")
        if (response?.data?.user?.mfaEnabled) {
          navigate('/mfa');
        } else {
          navigate('/dashboard');
        }
      }
    } catch (error) {
      console.error('Sign in error:', error);
      toast.error('Sign in failed. Please try again.');
    } finally {
      setIsSigningIn(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <div className="flex flex-col items-center space-y-6">
          {/* Logo */}
          <div className="w-24 h-24 bg-blue-500 rounded-full flex items-center justify-center">
            <LogIn className="w-12 h-12 text-white" />
          </div>

          <h1 className="text-2xl font-bold text-gray-800">Sign In</h1>

          {/* Sign In Form */}
          <form onSubmit={handleSubmit} className="w-full space-y-4">
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="email"
                placeholder="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full py-3 pl-10 pr-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400" />
              <input
                type="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full py-3 pl-10 pr-4 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full py-3 px-4 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition duration-300 ease-in-out flex items-center justify-center"
            >
              <LogIn className="w-5 h-5 mr-2" />
              Sign In
            </button>
          </form>
            <div onClick={onGoogleSignIn}>Sign In google</div>
          {/* Sign Up Link */}
          <p className="text-sm text-gray-600">
            Don't have an account?{" "}
            <a href="/signup" className="text-blue-500 hover:underline">
              Sign up
            </a>
          </p>
        </div>
      </div>
    </div>
  )
}

