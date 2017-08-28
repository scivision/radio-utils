function WBFMplot(fn,fs)
% Wideband FM demodulation and plotting of baseband multiplex spectrum
% Michael Hirsch, Ph.D.
%
% Especially useful for spectrum saved from RTL-SDR with GNU Radio, GQRX, etc.
  
try
  pkg load communications
end
  
sig = read_complex_binary(fn);

m = fmdemod(sig,fs);
  
end 