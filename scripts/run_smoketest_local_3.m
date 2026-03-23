addpath('C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\matlab\startup');
add_toolbox_paths;
clear all;
clc;

cfg = cfg_emoreg_defaults();

% ===== PATHS =====
cfg.paths.imagesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\Images\NAPS_H';
cfg.paths.scalesDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\SAM-Scales';
cfg.paths.resultsDir = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\outputs';
cfg.paths.assetsDir  = 'C:\Users\cns-co-admin\Desktop\fk\repos\neurotoolbox\assets';

cfg.task.manifestCsv = 'C:\Users\cns-co-admin\Desktop\fk\repos\cp_nonmotor\stimuli\blocks\pilot_block_112.csv';

cfg.trig.useTriggers = false;
cfg.el.useEyelink = false;

cfg.keys.useNumpad = true;

cfg.screen.screenNumber = 2;

% ===== LOAD MANIFEST =====
manifest = readtable(cfg.task.manifestCsv);

% ===== RUN TASK =====
Results = task_emoreg_run(cfg);