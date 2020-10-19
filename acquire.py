current_time = Time.now()

for i in range(0, 360, 5):
    print('i: '+str(i))

    # Get RA/Dec
    if i != 0:
        while Time.now() < current_time-(duration*u.second/2)+(1199.88*u.second): #1199.88*u.second):
            sleep(1)
    current_time = Time.now()
    print('[!] Time RIGHT NOW:')
    print(current_time)
    current_time = current_time+(duration*u.second/2)

    #Convert Alt/Az to RA/Dec
    AltAzcoordiantes = SkyCoord(alt = altitude*u.deg, az = 180*u.deg, obstime = current_time, frame = 'altaz', location = loc)
    c = AltAzcoordiantes.icrs

    ra = str(c.ra.hour) #[0:2].replace('h','')
    dec = str(c.dec.deg) #[0:3].replace('d','')
    print(ra,dec)
    with open('ra.txt', 'a') as f:
        f.write(ra+'\n')
    with open('dec.txt', 'a') as f:
        f.write(dec+'\n')

    # Data acquisition
    print('[+] Beginning observation...')
    virgo.observe(obs_parameters=observation, obs_file=str(i)+'.dat')
    print('[+] Obs done!')

    # Data analysis
    print('[+] Plotting...')
    virgo.plot(obs_parameters=observation, f_rest=1420.4057517667e6,
           obs_file=str(i)+'.dat', cal_file='calibration.dat',
           spectra_csv=str(i)+'.csv', plot_file=str(i)+'.png')
    print('[+] Plotting done!')

    # read from csv into record array
    df = np.genfromtxt(str(i)+'.csv',delimiter=',', usecols=(3))

    # calc means on columns
    mean_snr = np.nanmean(df, axis=0)
    print('[*] Mean SNR: '+str(mean_snr))
    with open('mean_snr.txt', 'a') as f:
        f.write(str(mean_snr)+'\n')
