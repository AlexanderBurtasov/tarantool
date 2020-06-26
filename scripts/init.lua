box.cfg {
    listen = 3313
}

box.once("bootstrap", function()
    box.schema.space.create('mystorage')
    box.space.mystorage:format({{'key', 'string'}, {'value', 'map'}})
    box.space.mystorage:create_index('primary', {type='hash', parts={'key'}})
end)
