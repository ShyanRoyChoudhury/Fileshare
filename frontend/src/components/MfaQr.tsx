
type Props = {
    qrCode: any

}

function MfaQr({qrCode}: Props) {

  return (
        <div className='p-6'>
            {qrCode? (
                <div>
                    <div>
                        <p>Scan & Enter OTP on Google Authenticator App to Enable 2FA Authentication</p>
                        <img src={qrCode} alt="QR Code"/>
                    </div>
                    
                </div>
            ):
            (<p>Loading QR Code..</p>)
            }
        </div>
  )
}

export default MfaQr

