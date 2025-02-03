"use client"

import { useState } from "react"
import { LogIn, Mail, Lock } from "lucide-react"
import { signInWithGoogle, doSignUpUserWithEmailAndPassword } from "../firebase/auth";
import { signInApi } from "../api/signInApi";
import { useNavigate } from "react-router-dom";
import { signUpApi } from "../api/signUpApi";
import { UserCredential } from "firebase/auth";

export default function SignUpPage() {

  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  const [ isSigningIn, setIsSigningIn ] = useState(false)
  const navigate = useNavigate();

  const onGoogleSignIn = async (_e: React.MouseEvent<HTMLDivElement>) => {
    if(!isSigningIn){
        setIsSigningIn(true);
        const userCredential: UserCredential = await signInWithGoogle();
        const idToken = await userCredential.user.getIdToken();
        const response = await signInApi(idToken);
        
        if (response?.data?.requireRegistration) {
          navigate('/signup');
        }
    }
  }

const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      setIsSigningIn(true);
      const userCredential = await doSignUpUserWithEmailAndPassword(email, password);
      const idToken = await userCredential.user.getIdToken();
      const userEmail = userCredential.user.email;

      if (!userEmail) {
        throw new Error('No email found for user');
      }
      if (idToken) {
        await signUpApi({ idToken, email: userEmail });
        navigate('/dashboard'); 
      }
    } catch (error) {
      console.error("Sign up error:", error);
    } finally {
      setIsSigningIn(false);
    }
  }


  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <div className="flex flex-col items-center space-y-6">
          {/* Logo */}
          <div className="w-24 h-24 bg-blue-500 rounded-full flex items-center justify-center">
            <LogIn className="w-12 h-12 text-white" />
          </div>

          <h1 className="text-2xl font-bold text-gray-800">Sign Up</h1>

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
            {/* <Link href="/signup" className="text-blue-500 hover:underline">
              Sign up
            </Link> */}
          </p>
        </div>
      </div>
    </div>
  )
}

