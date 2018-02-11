function RXplot(fn,fs, modtype,tss,fc)
% AM/FM demodulation and plotting of baseband multiplex spectrum
% Michael Hirsch, Ph.D.
%
% Especially useful for spectrum saved from RTL-SDR with GNU Radio, GQRX, etc.
%
% modtype: am  fm
% tss: start/stop times (seconds) to load (saves big time on enormous
% files)

try
  pkg load signal
end

nbits=16;
fsaudio = 48e3; % arbitrary for your soundcard
fmdev = 75e3; % scales audio by initial modulation
%% demodulation for complex signal
% NOTE: didn't filter cause assuming Nyquist bandwidth just enough for one
% station. Feel free to add filtering.
decim = fix(fs/fsaudio);

lstart = []; lcount = [];
if nargin>3 && ~isempty(tss)
  if length(tss)>=1
    lstart = fix(tss(1)*fs);
  end
  if length(tss)>=2
    lcount = fix(tss(2)*fs);
  end
end
sig = read_complex_binary(fn, lcount, lstart);
%% demodulation
switch lower(modtype)
    case 'fm'
        [m,t] = fmdemod_complex(sig, fs, fc, fmdev);
    case 'am'
        [m,t] = amdemod_complex(sig, fs, fc);
    otherwise
        error(['unknown modulation type ',modtype])
end
%% decimate
if ~isoctave
  m = double(m);
end
m = decimate(double(m), decim);
%% plot
figure(1)
plot(t(1:decim:end),m)
xlabel('time [sec]')
ylabel('amplitude')
title([upper(modtype),' demodulated audio'])

figure(2),clf(2)
if isoctave
    center = 'centerdc';
else
    center = 'centered';
end
pwelch(sig,[],[],[],fs,center)
%% audio playback
% normalize so that you can hear it
m = m/max(m);
h = audioplayer(m, fsaudio, nbits);
playblocking(h)  % just play() will stop after fraction of a second
end % function