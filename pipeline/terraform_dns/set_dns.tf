resource "mikrotik_dns_record" "myevents_sandbox" {
  name    = "myevents.sandbox.altmeyer.local"
  address = "10.10.3.51"
  ttl     = 300
}

resource "mikrotik_dns_record" "myevents_production" {
  name    = "myevents.production.altmeyer.local"
  address = "10.10.3.81"
  ttl     = 300
}

resource "mikrotik_dns_record" "myevents_production_simple" {
  name    = "myevents.altmeyer.local"
  address = "10.10.3.81"
  ttl     = 300
}
