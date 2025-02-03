import { sendEmailVerification, getAuth } from "firebase/auth";
import { useLocation, useNavigate } from "react-router-dom";

function VerifyEmail() {
  const location = useLocation();
  const user = location.state?.user; // Extract user details
  
  const handleVerify = async () => {
    if (!user) return;
    
    const auth = getAuth();
    const currentUser = auth.currentUser; // Get the currently authenticated user
    const navigate = useNavigate();
    if (currentUser && currentUser.uid === user.uid) {
      await sendEmailVerification(currentUser);
      alert("Verification email sent!");
      navigate('/signin');
    } else {
      alert("User not authenticated. Please log in again.");
    }
  };

  return (
    <div>
      <h1>Verify Your Email</h1>
      {user && <p>Signed up as: {user.email}</p>}
      <div onClick={handleVerify} className="bg-white cursor pointer p-4">Click to Send Email Verification Link</div>
    </div>
  );
}

export default VerifyEmail;