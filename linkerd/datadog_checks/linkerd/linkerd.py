# (C) Datadog, Inc. 2018
# All rights reserved
# Licensed under a 3-clause BSD style license (see LICENSE)

# stdlib

# 3rd party
import requests

# project
from datadog_checks.checks.prometheus import PrometheusCheck

EVENT_TYPE = SOURCE_TYPE_NAME = 'linkerd'

PROMETHEUS_ENDPOINT = '/admin/metrics/prometheus'
PING_ENDPOINT = '/admin/ping'

SERVICE_CHECK_NAME = 'linkerd.can_connect'

class LinkerdCheck(PrometheusCheck):
    """
    Collect linkerd metrics from Prometheus
    """
    def __init__(self, name, init_config, agentConfig, instances=None):
        super(LinkerdCheck, self).__init__(name, init_config, agentConfig, instances)
        self.NAMESPACE = 'linkerd'

        self.metrics_mapper = {}
        self.type_overrides = {}

        metrics_map = {
            'jvm:start_time': 'jvm.start_time',
            'jvm:application_time_millis': 'jvm.application_time_millis',
            'jvm:classes:total_loaded': 'jvm.classes.total_loaded',
            'jvm:classes:current_loaded': 'jvm.classes.current_loaded',
            'jvm:classes:total_unloaded': 'jvm.classes.total_unloaded',
            'jvm:postGC:Par_Survivor_Space:max': 'jvm.postGC.Par_Survivor_Space.max',
            'jvm:postGC:Par_Survivor_Space:used': 'jvm.postGC.Par_Survivor_Space.used',
            'jvm:postGC:CMS_Old_Gen:max': 'jvm.postGC.CMS_Old_Gen.max',
            'jvm:postGC:CMS_Old_Gen:used': 'jvm.postGC.CMS_Old_Gen.used',
            'jvm:postGC:Par_Eden_Space:max': 'jvm.postGC.Par_Eden_Space.max',
            'jvm:postGC:Par_Eden_Space:used': 'jvm.postGC.Par_Eden_Space.used',
            'jvm:postGC:used': 'jvm.postGC.used',
            'jvm:nonheap:committed': 'jvm.nonheap.committed',
            'jvm:nonheap:max': 'jvm.nonheap.max',
            'jvm:nonheap:used': 'jvm.nonheap.used',
            'jvm:tenuring_threshold': 'jvm.tenuring_threshold',
            'jvm:thread:count': 'jvm.thread.count',
            'jvm:mem:postGC:Par_Survivor_Space:max': 'jvm.mem.postGC.Par_Survivor_Space.max',
            'jvm:mem:postGC:Par_Survivor_Space:used': 'jvm.mem.postGC.Par_Survivor_Space.used',
            'jvm:mem:postGC:CMS_Old_Gen:max': 'jvm.mem.postGC.CMS_Old_Gen.max',
            'jvm:mem:postGC:CMS_Old_Gen:used': 'jvm.mem.postGC.CMS_Old_Gen.used',
            'jvm:mem:postGC:Par_Eden_Space:max': 'jvm.mem.postGC.Par_Eden_Space.max',
            'jvm:mem:postGC:Par_Eden_Space:used': 'jvm.mem.postGC.Par_Eden_Space.used',
            'jvm:mem:postGC:used': 'jvm.mem.postGC.used',
            'jvm:mem:metaspace:max_capacity': 'jvm.mem.metaspace.max_capacity',
            'jvm:mem:buffer:direct:max': 'jvm.mem.buffer.direct.max',
            'jvm:mem:buffer:direct:count': 'jvm.mem.buffer.direct.count',
            'jvm:mem:buffer:direct:used': 'jvm.mem.buffer.direct.used',
            'jvm:mem:buffer:mapped:max': 'jvm.mem.buffer.mapped.max',
            'jvm:mem:buffer:mapped:count': 'jvm.mem.buffer.mapped.count',
            'jvm:mem:buffer:mapped:used': 'jvm.mem.buffer.mapped.used',
            'jvm:mem:allocations:eden:bytes': 'jvm.mem.allocations.eden.bytes',
            'jvm:mem:current:used': 'jvm.mem.current.used',
            'jvm:mem:current:CMS_Old_Gen:max': 'jvm.mem.current.CMS_Old_Gen.max',
            'jvm:mem:current:CMS_Old_Gen:used': 'jvm.mem.current.CMS_Old_Gen.used',
            'jvm:mem:current:Metaspace:max': 'jvm.mem.current.Metaspace.max',
            'jvm:mem:current:Metaspace:used': 'jvm.mem.current.Metaspace.used',
            'jvm:mem:current:Par_Eden_Space:max': 'jvm.mem.current.Par_Eden_Space.max',
            'jvm:mem:current:Par_Eden_Space:used': 'jvm.mem.current.Par_Eden_Space.used',
            'jvm:mem:current:Par_Survivor_Space:max': 'jvm.mem.current.Par_Survivor_Space.max',
            'jvm:mem:current:Par_Survivor_Space:used': 'jvm.mem.current.Par_Survivor_Space.used',
            'jvm:mem:current:Compressed_Class_Space:max': 'jvm.mem.current.Compressed_Class_Space.max',
            'jvm:mem:current:Compressed_Class_Space:used': 'jvm.mem.current.Compressed_Class_Space.used',
            'jvm:mem:current:Code_Cache:max': 'jvm.mem.current.Code_Cache.max',
            'jvm:mem:current:Code_Cache:used': 'jvm.mem.current.Code_Cache.used',
            'jvm:num_cpus': 'jvm.num_cpus',
            'jvm:gc:msec': 'jvm.gc.msec',
            'jvm:gc:eden:pause_msec_avg': 'jvm.gc.eden.pause_msec_avg',
            'jvm:gc:ParNew:msec': 'jvm.gc.ParNew.msec',
            'jvm:gc:ParNew:cycles': 'jvm.gc.ParNew.cycles',
            'jvm:gc:ConcurrentMarkSweep:msec': 'jvm.gc.ConcurrentMarkSweep.msec',
            'jvm:gc:ConcurrentMarkSweep:cycles': 'jvm.gc.ConcurrentMarkSweep.cycles',
            'jvm:gc:cycles': 'jvm.gc.cycles',
            'jvm:fd_limit': 'jvm.fd_limit',
            'jvm:compilation:time_msec': 'jvm.compilation.time_msec',
            'jvm:uptime': 'jvm.uptime',
            'jvm:safepoint:sync_time_millis': 'jvm.safepoint.sync_time_millis',
            'jvm:safepoint:total_time_millis': 'jvm.safepoint.total_time_millis',
            'jvm:safepoint:count': 'jvm.safepoint.count',
            'jvm:heap:committed': 'jvm.heap.committed',
            'jvm:heap:max': 'jvm.heap.max',
            'jvm:heap:used': 'jvm.heap.used',
            'rt:client:connect_latency_ms_avg': 'rt.client.connect_latency_ms_avg',
            'rt:client:failed_connect_latency_ms_avg': 'rt.client.failed_connect_latency_ms_avg',
            'rt:client:sent_bytes': 'rt.client.sent_bytes',
            'rt:client:service_creation:service_acquisition_latency_ms_avg': 'rt.client.service_creation.service_acquisition_latency_ms_avg',
            'rt:client:connection_received_bytes_avg': 'rt.client.connection_received_bytes_avg',
            'rt:client:connection_duration_avg': 'rt.client.connection_duration_avg',
            'rt:client:failure_accrual:removals': 'rt.client.failure_accrual.removals',
            'rt:client:failure_accrual:probes': 'rt.client.failure_accrual.probes',
            'rt:client:failure_accrual:removed_for_ms': 'rt.client.failure_accrual.removed_for_ms',
            'rt:client:failure_accrual:revivals': 'rt.client.failure_accrual.revivals',
            'rt:client:connects': 'rt.client.connects',
            'rt:client:pool_num_waited': 'rt.client.pool_num_waited',
            'rt:client:success': 'rt.client.success',
            'rt:client:request_latency_ms_avg': 'rt.client.request_latency_ms_avg',
            'rt:client:pool_waiters': 'rt.client.pool_waiters',
            'rt:client:retries:requeues_per_request_avg': 'rt.client.retries.requeues_per_request_avg',
            'rt:client:retries:request_limit': 'rt.client.retries.request_limit',
            'rt:client:retries:budget_exhausted': 'rt.client.retries.budget_exhausted',
            'rt:client:retries:cannot_retry': 'rt.client.retries.cannot_retry',
            'rt:client:retries:not_open': 'rt.client.retries.not_open',
            'rt:client:retries:budget': 'rt.client.retries.budget',
            'rt:client:retries:requeues': 'rt.client.retries.requeues',
            'rt:client:received_bytes': 'rt.client.received_bytes',
            'rt:client:read_timeout': 'rt.client.read_timeout',
            'rt:client:write_timeout': 'rt.client.write_timeout',
            'rt:client:connection_sent_bytes_avg': 'rt.client.connection_sent_bytes_avg',
            'rt:client:connection_requests_avg': 'rt.client.connection_requests_avg',
            'rt:client:service:success': 'rt.client.service.success',
            'rt:client:service:request_latency_ms_avg': 'rt.client.service.request_latency_ms_avg',
            'rt:client:service:failures': 'rt.client.service.failures',
            'rt:client:service:requests': 'rt.client.service.requests',
            'rt:client:service:pending': 'rt.client.service.pending',
            'rt:client:pool_num_too_many_waiters': 'rt.client.pool_num_too_many_waiters',
            'rt:client:socket_unwritable_ms': 'rt.client.socket_unwritable_ms',
            'rt:client:closes': 'rt.client.closes',
            'rt:client:pool_cached': 'rt.client.pool_cached',
            'rt:client:nack_admission_control:dropped_requests': 'rt.client.nack_admission_control.dropped_requests',
            'rt:client:status:1XX': 'rt.client.status.1XX',
            'rt:client:status:4XX': 'rt.client.status.4XX',
            'rt:client:status:2XX': 'rt.client.status.2XX',
            'rt:client:status:error': 'rt.client.status.error',
            'rt:client:status:3XX': 'rt.client.status.3XX',
            'rt:client:status:5XX': 'rt.client.status.5XX',
            'rt:client:failures': 'rt.client.failures',
            'rt:client:pool_size': 'rt.client.pool_size',
            'rt:client:available': 'rt.client.available',
            'rt:client:time:1XX_avg': 'rt.client.time.1XX_avg',
            'rt:client:time:4XX_avg': 'rt.client.time.4XX_avg',
            'rt:client:time:2XX_avg': 'rt.client.time.2XX_avg',
            'rt:client:time:error_avg': 'rt.client.time.error_avg',
            'rt:client:time:3XX_avg': 'rt.client.time.3XX_avg',
            'rt:client:time:5XX_avg': 'rt.client.time.5XX_avg',
            'rt:client:socket_writable_ms': 'rt.client.socket_writable_ms',
            'rt:client:cancelled_connects': 'rt.client.cancelled_connects',
            'rt:client:pending': 'rt.client.pending',
            'rt:client:dispatcher:serial:queue_size': 'rt.client.dispatcher.serial.queue_size',
            'rt:client:dispatcher:stream:failures': 'rt.client.dispatcher.stream.failures',
            'rt:client:connections': 'rt.client.connections',
            'rt:client:requests': 'rt.client.requests',
            'rt:client:service:requests': 'rt.client.service.requests',
            'rt:server:requests': 'rt.server.requests',

            'rt:server:request_latency_ms': 'rt.server.request_latency_ms',
            'rt:client:connect_latency_ms': 'rt.client.connect_latency_ms',
            'rt:client:failed_connect_latency_ms': 'rt.client.failed_connect_latency_ms',
            'rt:client:service_creation:service_acquisition_latency_ms': 'rt.client.service_creation.service_acquisition_latency_ms',
            'rt:client:connection_received_bytes': 'rt.client.connection_received_bytes',
            'rt:client:connection_duration': 'rt.client.connection_duration',
            'rt:client:request_latency_ms': 'rt.client.request_latency_ms',
            'rt:client:retries:requeues_per_request': 'rt.client.retries.requeues_per_request',
            'rt:client:connection_sent_bytes': 'rt.client.connection_sent_bytes',
            'rt:client:connection_requests': 'rt.client.connection_requests',
            'rt:client:service:request_latency_ms': 'rt.client.service.request_latency_ms',
            'rt:client:time:1XX': 'rt.client.time.1XX',
            'rt:client:time:4XX': 'rt.client.time.4XX',
            'rt:client:time:2XX': 'rt.client.time.2XX',
            'rt:client:time:error': 'rt.client.time.error',
            'rt:client:time:3XX': 'rt.client.time.3XX',
            'rt:client:time:5XX': 'rt.client.time.5XX',
            'rt:client:dtab:size': 'rt.client.dtab.size',
            'jvm:gc:eden:pause_msec': 'jvm.gc.eden.pause_msec',
        }

        types_map = {
            'jvm:start_time': 'gauge',
            'jvm:application_time_millis': 'gauge',
            'jvm:classes:total_loaded': 'gauge',
            'jvm:classes:current_loaded': 'gauge',
            'jvm:classes:total_unloaded': 'gauge',
            'jvm:postGC:Par_Survivor_Space:max': 'gauge',
            'jvm:postGC:Par_Survivor_Space:used': 'gauge',
            'jvm:postGC:CMS_Old_Gen:max': 'gauge',
            'jvm:postGC:CMS_Old_Gen:used': 'gauge',
            'jvm:postGC:Par_Eden_Space:max': 'gauge',
            'jvm:postGC:Par_Eden_Space:used': 'gauge',
            'jvm:postGC:used': 'gauge',
            'jvm:nonheap:committed': 'gauge',
            'jvm:nonheap:max': 'gauge',
            'jvm:nonheap:used': 'gauge',
            'jvm:tenuring_threshold': 'gauge',
            'jvm:thread:count': 'gauge',
            'jvm:mem:postGC:Par_Survivor_Space:max': 'gauge',
            'jvm:mem:postGC:Par_Survivor_Space:used': 'gauge',
            'jvm:mem:postGC:CMS_Old_Gen:max': 'gauge',
            'jvm:mem:postGC:CMS_Old_Gen:used': 'gauge',
            'jvm:mem:postGC:Par_Eden_Space:max': 'gauge',
            'jvm:mem:postGC:Par_Eden_Space:used': 'gauge',
            'jvm:mem:postGC:used': 'gauge',
            'jvm:mem:metaspace:max_capacity': 'gauge',
            'jvm:mem:buffer:direct:max': 'gauge',
            'jvm:mem:buffer:direct:count': 'gauge',
            'jvm:mem:buffer:direct:used': 'gauge',
            'jvm:mem:buffer:mapped:max': 'gauge',
            'jvm:mem:buffer:mapped:count': 'gauge',
            'jvm:mem:buffer:mapped:used': 'gauge',
            'jvm:mem:allocations:eden:bytes': 'gauge',
            'jvm:mem:current:used': 'gauge',
            'jvm:mem:current:CMS_Old_Gen:max': 'gauge',
            'jvm:mem:current:CMS_Old_Gen:used': 'gauge',
            'jvm:mem:current:Metaspace:max': 'gauge',
            'jvm:mem:current:Metaspace:used': 'gauge',
            'jvm:mem:current:Par_Eden_Space:max': 'gauge',
            'jvm:mem:current:Par_Eden_Space:used': 'gauge',
            'jvm:mem:current:Par_Survivor_Space:max': 'gauge',
            'jvm:mem:current:Par_Survivor_Space:used': 'gauge',
            'jvm:mem:current:Compressed_Class_Space:max': 'gauge',
            'jvm:mem:current:Compressed_Class_Space:used': 'gauge',
            'jvm:mem:current:Code_Cache:max': 'gauge',
            'jvm:mem:current:Code_Cache:used': 'gauge',
            'jvm:num_cpus': 'gauge',
            'jvm:gc:msec': 'gauge',
            'jvm:gc:eden:pause_msec_avg': 'gauge',
            'jvm:gc:ParNew:msec': 'gauge',
            'jvm:gc:ParNew:cycles': 'gauge',
            'jvm:gc:ConcurrentMarkSweep:msec': 'gauge',
            'jvm:gc:ConcurrentMarkSweep:cycles': 'gauge',
            'jvm:gc:cycles': 'gauge',
            'jvm:fd_limit': 'gauge',
            'jvm:compilation:time_msec': 'gauge',
            'jvm:uptime': 'gauge',
            'jvm:safepoint:sync_time_millis': 'gauge',
            'jvm:safepoint:total_time_millis': 'gauge',
            'jvm:safepoint:count': 'gauge',
            'jvm:heap:committed': 'gauge',
            'jvm:heap:max': 'gauge',
            'jvm:heap:used': 'gauge',
            'rt:client:connect_latency_ms_avg': 'gauge',
            'rt:client:failed_connect_latency_ms_avg': 'gauge',
            'rt:client:sent_bytes': 'gauge',
            'rt:client:service_creation:service_acquisition_latency_ms_avg': 'gauge',
            'rt:client:connection_received_bytes_avg': 'gauge',
            'rt:client:connection_duration_avg': 'gauge',
            'rt:client:failure_accrual:removals': 'gauge',
            'rt:client:failure_accrual:probes': 'gauge',
            'rt:client:failure_accrual:removed_for_ms': 'gauge',
            'rt:client:failure_accrual:revivals': 'gauge',
            'rt:client:connects': 'gauge',
            'rt:client:pool_num_waited': 'gauge',
            'rt:client:success': 'gauge',
            'rt:client:request_latency_ms_avg': 'gauge',
            'rt:client:pool_waiters': 'gauge',
            'rt:client:retries:requeues_per_request_avg': 'gauge',
            'rt:client:retries:request_limit': 'gauge',
            'rt:client:retries:budget_exhausted': 'gauge',
            'rt:client:retries:cannot_retry': 'gauge',
            'rt:client:retries:not_open': 'gauge',
            'rt:client:retries:budget': 'gauge',
            'rt:client:retries:requeues': 'gauge',
            'rt:client:received_bytes': 'gauge',
            'rt:client:read_timeout': 'gauge',
            'rt:client:write_timeout': 'gauge',
            'rt:client:connection_sent_bytes_avg': 'gauge',
            'rt:client:connection_requests_avg': 'gauge',
            'rt:client:service:success': 'gauge',
            'rt:client:service:request_latency_ms_avg': 'gauge',
            'rt:client:service:failures': 'gauge',
            'rt:client:service:requests': 'gauge',
            'rt:client:service:pending': 'gauge',
            'rt:client:pool_num_too_many_waiters': 'gauge',
            'rt:client:socket_unwritable_ms': 'gauge',
            'rt:client:closes': 'gauge',
            'rt:client:pool_cached': 'gauge',
            'rt:client:nack_admission_control:dropped_requests': 'gauge',
            'rt:client:status:1XX': 'gauge',
            'rt:client:status:4XX': 'gauge',
            'rt:client:status:2XX': 'gauge',
            'rt:client:status:error': 'gauge',
            'rt:client:status:3XX': 'gauge',
            'rt:client:status:5XX': 'gauge',
            'rt:client:failures': 'gauge',
            'rt:client:pool_size': 'gauge',
            'rt:client:available': 'gauge',
            'rt:client:time:1XX_avg': 'gauge',
            'rt:client:time:4XX_avg': 'gauge',
            'rt:client:time:2XX_avg': 'gauge',
            'rt:client:time:error_avg': 'gauge',
            'rt:client:time:3XX_avg': 'gauge',
            'rt:client:time:5XX_avg': 'gauge',
            'rt:client:socket_writable_ms': 'gauge',
            'rt:client:cancelled_connects': 'gauge',
            'rt:client:pending': 'gauge',
            'rt:client:dispatcher:serial:queue_size': 'gauge',
            'rt:client:dispatcher:stream:failures': 'gauge',
            'rt:client:connections': 'gauge',
            'rt:client:requests': 'gauge',
            'rt:server:requests': 'gauge',

            'jvm:gc:eden:pause_msec': 'summary',
            'rt:server:request_latency_ms': 'summary',
            'rt:client:connect_latency_ms': 'summary',
            'rt:client:failed_connect_latency_ms': 'summary',
            'rt:client:service_creation:service_acquisition_latency_ms': 'summary',
            'rt:client:connection_received_bytes': 'summary',
            'rt:client:connection_duration': 'summary',
            'rt:client:request_latency_ms': 'summary',
            'rt:client:retries:requeues_per_request': 'summary',
            'rt:client:connection_sent_bytes': 'summary',
            'rt:client:connection_requests': 'summary',
            'rt:client:service:request_latency_ms': 'summary',
            'rt:client:time:1XX': 'summary',
            'rt:client:time:4XX': 'summary',
            'rt:client:time:2XX': 'summary',
            'rt:client:time:error': 'summary',
            'rt:client:time:3XX': 'summary',
            'rt:client:time:5XX': 'summary',
            'rt:client:dtab:size': 'summary',
        }

        # Linkerd allows you to add a prefix for the metrics in the configuration
        prefix = self.init_config.get("linkerd_prometheus_prefix", '')
        for m in metrics_map:
            self.metrics_mapper[prefix + m] = metrics_map[m]
        for m in types_map:
            self.type_overrides[prefix + m] = types_map[m]


    def _finalize_tags_to_submit(self, _tags, metric_name, val, metric, custom_tags=None, hostname=None):
        return _tags

    def check(self, instance):
        admin_ip = instance.get('admin_ip')
        admin_port = instance.get('admin_port')

        if admin_ip is None or admin_port is None:
            raise Exception("Unable to find admin_ip and admin_port in config file.")


        prometheus_url = "http://{}:{}{}".format(
            admin_ip,
            admin_port,
            PROMETHEUS_ENDPOINT
        )

        ping_url = "http://{}:{}{}".format(
            admin_ip,
            admin_port,
            PING_ENDPOINT
        )

        tags = ["linkerd_admin_ip:{}".format(admin_ip), "linkerd_admin_port:{}".format(admin_port)]

        try:
            r = requests.get(ping_url)
            r.raise_for_status()
            if r.content == "pong":
                self.service_check(SERVICE_CHECK_NAME, PrometheusCheck.OK,
                               tags=tags)
            else:
                self.service_check(SERVICE_CHECK_NAME, PrometheusCheck.UNKNOWN,
                               tags=tags)
                raise Exception("Error pinging {}. Server responded with: {}".format(PING_ENDPOINT, r.content))
        except requests.exceptions.HTTPError as e:
            self.service_check(SERVICE_CHECK_NAME, PrometheusCheck.CRITICAL,
                               tags=tags)
            raise Exception("Error pinging {}. Error: {}".format(PING_ENDPOINT, e))

        self.process(prometheus_url, send_histograms_buckets=True, instance=instance)
