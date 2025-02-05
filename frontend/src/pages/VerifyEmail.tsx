import { sendEmailVerification, getAuth } from "firebase/auth";
import { useLocation, useNavigate } from "react-router-dom";

function VerifyEmail() {
  const location = useLocation();
  const user = location.state?.user; // Extract user details
  const navigate = useNavigate();
  
  const handleVerify = async () => {
    if (!user) return;
    
    const auth = getAuth();
    const currentUser = auth.currentUser; // Get the currently authenticated user
    if (currentUser && currentUser.uid === user.uid) {
      await sendEmailVerification(currentUser);
      alert("Verification email sent!");
      navigate('/');
    } else {
      alert("User not authenticated. Please log in again.");
    }
  };

  return (
    <div className="p-20 space-y-4">
      <div className="mx-auto">
        <h1 className=" text-white font-semibold text-3xl">Verify Your Email</h1>
        {user && <p>Signed up as: {user.email}</p>}
        <button onClick={handleVerify} className="bg-white rounded-md cursor pointer p-4 text-lg hover:bg-gray-400">Click to Send Email Verification Link</button>
      </div>
    </div>
  );
}

export default VerifyEmail;