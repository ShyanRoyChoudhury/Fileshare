import { createContext, useEffect, useState } from "react";
import { onAuthStateChanged, User } from "firebase/auth";
import { auth } from "../../config/firebase-config";

type AuthContextType = {
    currentUser: User | null;
    userLoggedIn: boolean;
    loading: boolean;
  };
  
  const AuthContext = createContext<AuthContextType>({
    currentUser: null,
    userLoggedIn: false,
    loading: true
});

export function AuthProvider({ children }: any) {
    const [currentUser, setCurrentUser] = useState(null);
    const [userLoggedIn, setUserLoggedIn] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(()=> {
        const unsubsribe = onAuthStateChanged(auth, initializeUser)
        return unsubsribe;
    }, [])

    async function initializeUser(user: any){
        if(user){
            setCurrentUser({ ...user });
            setUserLoggedIn(true);
        }else{
            setCurrentUser(null);
            setUserLoggedIn(false);
        }
        setLoading(false)
    }

    const value = {
        currentUser, userLoggedIn, loading
    }
    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    )
}