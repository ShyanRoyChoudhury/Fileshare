import React, { createContext, useEffect, useState } from "react";
import { auth } from "../../config/firebase-config";
import { onAuthStateChanged } from "firebase/auth";

const AuthContext = createContext();

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