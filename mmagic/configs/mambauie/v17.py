"""
defaultdict(<class 'float'>, {'conv': 0.4644864, 'layer_norm': 0.635904, 'linear': 5.330571264, 'einsum': 1.68092, 'PythonOp.SelectiveScanFn': 2.5655312})
params 153700 GFLOPs 10.677412864
"""

_base_ = [
    './seamamba.py'
]

ver = 'v17'
experiment_name = f'seamamba_uieb_{ver}'
work_dir = f'./work_dirs/{experiment_name}'
save_dir = './work_dirs/'

# model settings
model = dict(
    type='BaseEditModel',
    generator=dict(
        _delete_=True,
        type='MM_VSSM',
        depths=[1]*4,
        dims=[48]*4,
        ver=ver,
    ))

batch_size = 32
train_dataloader = dict(batch_size=batch_size)
val_dataloader = dict(batch_size=batch_size)

optim_wrapper = dict(
    dict(
        type='AmpOptimWrapper',
        optimizer=dict(type='AdamW', lr=0.0002, betas=(0.9, 0.999), weight_decay=0.5)))

max_epochs = 800
param_scheduler = [
    dict(
        type='LinearLR', start_factor=0.001, by_epoch=True, begin=0,
        end=15),
    dict(type='CosineAnnealingLR', by_epoch=True, T_max=max_epochs, convert_to_iter_based=True),]

train_cfg = dict(by_epoch=True, max_epochs=max_epochs)

visualizer = dict(
    vis_backends=[dict(type='LocalVisBackend'), dict(type='WandbVisBackend', init_kwargs=dict(project='seamamba', name=ver))])

auto_scale_lr = dict(enable=False)
default_hooks = dict(logger=dict(interval=5))
custom_hooks = [dict(type='BasicVisualizationHook', interval=3)]
