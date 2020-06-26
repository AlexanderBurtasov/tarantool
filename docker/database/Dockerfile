FROM tarantool/tarantool:2.2.0 as tarantool

MAINTAINER Alexander Burtasov "pvt.pyle1983@gmail.com"

COPY scripts/init.lua /opt/tarantool
RUN chmod ugo-x /opt/tarantool/init.lua

CMD ["tarantool", "/opt/tarantool/init.lua"]
