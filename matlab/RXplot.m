function RXplot(fn,fs,modtype,tss)
% AM/FM demodulation and plotting of baseband multiplex spectrum
% Michael Hirsch, Ph.D.
%
% Especially useful for spectrum saved from RTL-SDR with GNU Radio, GQRX, etc.
%
% modtype: am  fm
% tss: start/stop times (seconds) to load (saves big time on enormous
% files)
  
nbits=16;
fsaudio = 48e3; % arbitrary for your soundcard
fc = [];  % frequency offset from center ( [] to ignore)
fmdev = 75e3; % scales audio by initial modulation
%% demodulation for complex signal
% NOTE: didn't filter cause assuming Nyquist bandwidth just enough for one
% station. Feel free to add filtering.
decim = fix(fs/fsaudio);

if length(tss)>=1
    lstart = fix(tss(1)*fs);
else
    lstart = [];
end
if length(tss)>=2
    lcount = fix(tss(2)*fs);
else
    lcount = [];
end
sig = read_complex_binary(fn, lcount, lstart);

switch lower(modtype)
    case 'fm'
        [m,t] = fmdemod_complex(sig,fs, fc, fmdev);
    case 'am'
        [m,t] = amdemod_complex(sig, fs, fc);
    otherwise
        error(['unknown modulation type ',modtype])
end
        
m = decimate(double(m), decim);
%%
figure(1)
plot(t(1:decim:end),m)
xlabel('time [sec]')
ylabel('amplitude')
title([upper(modtype),' demodulated audio'])
%% audio playback
% normalize so that you can hear it
m = m/max(m);
h = audioplayer(m, fsaudio, nbits);
playblocking(h)  % just play() will stop after fraction of a second
end 