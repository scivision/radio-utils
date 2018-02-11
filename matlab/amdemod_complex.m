function [m,t] = amdemod_complex(y, fs, fc)
%AMDEMOD Amplitude demodulation of complex IQ baseband.
% if you prefer LPF demodulation, see https://sourceforge.net/p/octave/communications/ci/default/tree/inst/amdemod.m

narginchk(1,3)
assert(isvector(y),'expecting complex IQ samples vector, amplitude modulation')

y = y(:);

t =(0:length(y)-1) / fs;
%% freq shift if necessary
if nargin>2
    y = y .* exp(-1i*2*pi*fc*t).';    
end % if

%y = filtfilt(b, 1, y); % channel filter (keep out adjacent stations, optional)
m = real(y.^2); % ideal diode

end % function