import { Config } from '@remotion/cli/config';
Config.setBrowserExecutable('/opt/pw-browsers/chromium');
Config.setChromiumOpenGlRenderer('swangle');
Config.setChromiumDisableWebSecurity(false);
Config.setConcurrency(2);
Config.setVideoImageFormat('jpeg');
