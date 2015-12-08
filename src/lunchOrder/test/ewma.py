import qrcode

img = qrcode.make('Some data here')
###


if __name__ == '__main__':
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data('Some data')
    qr.make(fit=True)
    
    img = qr.make_image()   
    print img 