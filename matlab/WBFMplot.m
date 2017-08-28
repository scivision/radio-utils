function WBFMplot(fn,fs)
% Wideband FM demodulation and plotting of baseband multiplex spectrum
% Michael Hirsch, Ph.D.
%
% Especially useful for spectrum saved from RTL-SDR with GNU Radio, GQRX, etc.
  
try
  pkg load communications
end
 
nbits=16;
fsaudio = 48e3; % arbitrary for your soundcard
fc = [];  % frequency offset from center ( [] to ignore)
fmdev = 100e3; % scales audio by initial modulation
%% 
decim = fix(fs/fsaudio);
  
sig = read_complex_binary(fn);

[m,t] = fmdemod_complex(sig,fs, fc, fmdev);
m = decimate(double(m), decim);
%%
plot(t(1:decim:end),m)
xlabel('time [sec]')
ylabel('amplitude')
title('FM demodulated audio')
%% 
h = audioplayer(m,fsaudio,nbits);
play(h)  % just play() will stop after fraction of a second
end 