s = box.schema.space.create('storage')
s:format({{name='key', type='string'}, {name='value', type='map'}})
s:create_index('primary', {type='hash', parts={'key'}})
