---
author: ["Olivia Snowden"]
title: "BUILDING LOAD BALANCERS IN GCP WITH TERRAFORM"
date: "2023-03-22"
tags: ["code", "terraform", "networking", "gcp", "cloud"]
ShowToc: true
TocOpen: true
---
![](/building-a-lb-with-tf-logo.png)

Networking in GCP, or any cloud environment, often requires a load balancer(LB). If you try to use Terraform to deploy a load balancer in GCP you'll notice that there is not a single Terraform resource to create a GCP LB. GCP provides example Terraform scripts to create LBs in their documentation [here](https://cloud.google.com/load-balancing/docs/load-balancing-overview). 

However, if you have an understanding of how load balancers work internally, and how to properly structure your Terraform code, creating your own LB modules in GCP using Terraform is possible. This can allow you to configure your LBs to do exactly what you need.  

## What is a Load Balancer? 
Load balancers are networking resources that take in network traffic through their frontend and distribute that traffic to their backend(s). Load balancers have a few basic parts you should know:
- **Frontend** 
  Where clients reach the load balancer, the "face" of the load balancer.
- **Backend**
  The server(s) where the load balancer directs traffic
- **Forwarding Rules**
  The logic the load balancer uses to distribute traffic. Also referred to as a load balancer's "algorithm".
- **Health Checks**
  Checks the status of the backend(s) and whether they can recieve traffic. Load balancers will not send traffic to an unhealthy backend.

  Below is a simple diagram that illustrates the flow of traffic through a load balancer:
![](/building-a-lb-w-tf.jpeg)

Traffic enters the load balancer through its frontend IP, the forwarding rule(s) determines how to route traffic to the backends, the health check confirms that the backend is healthy-and if so then the traffic is routed there.

### Rules
Deciding how to route traffic to a load balancer's backends depends on the use case. For example, if a network admin has 2 servers and server 1 can handle more requests than server 2, then the load balancer can be configured to use a weighted rule which will send more traffic to server 1.

However if a network admin has 2 servers with the same processing power they can confgure the load balancer to use a least connection rule which will send traffic to the server that is the most available at the time.

## GCP Load Balancers
Load balancers can exist in the cloud as well as on-premises networks. This post will primarily focus on internal/external TCP/HTTPS cloud-based load balancers in GCP, although similar load balancers exist in AWS and Azure cloud platforms. Load balancers in GCP work just like load balancers in any other network, with the exception that some or all of the traffic of GCP load balancers is between GCP cloud resources.

When creating a load balancer  in GCP, it is important to understand the different types of load balancers supported.

### Internal and External Load Balancers 
GCP supports 2 options for the IP address of their load balancers, internal and external.

Internal LBs only distribute traffic to resources within GCP. External LBs route traffic coming from the internet into GCP. It is important to note that external LBs often require additional security measures due to the LBs being public-facing.

### TCP/UDP and HTTP(S) Load Balancers
GCP supports 4 types of traffic on their load balancers: TCP, UDP, HTTP(S), and SSL. This post will primarily focus on TCP/UDP and HTTP(S) load balancing.

## Creating a Load Balancer using Terraform
Load balancers can be created in GCP using Terraform, however there is not a single Terraform resource that creates a load balancer. Instead, multiple Terraform resources together create a GCP load balancer. These resources include:

- **"google_compute_global_address"**    = The public IP address that is the frontend of the LB. (External LBs only)
  
- **"google_compute_target_http_proxy"** = Routes requests to the url map (**"google_compute_global_forwarding_rule"** for external LBs)
  
- **"google_compute_url_map"**           = Defines the rules to route traffic to the backend

- **"google_compute_forwarding_rule"**   = Routes traffic to the backends

- **"google_compute_backend_service"**   = Creates the LB's backend(s)
  
- **"google_compute_health_check"**      = The LB's health check (optiona)

Note, that the global address and http proxy resources are different between internal and external LBs. External LBs use a global address resource to make a public IP address that clients from the internet can use to access the external LB. Internal LBs do not need a global address. In addiiton, internal LBs use the **"google_compute_target_http_proxy"** proxy resource, external LBs use the **"google_compute_global_forwarding_rule"** resource. 

Below is a diagram illustrating the flow of traffic through the Terraform resources that make an internal load balancer: 
![](/building-a-lb-with-tf-ilb.jpeg)

And this is the flow of traffic through the Terraform resources that make an external load balancer: 
![](/building-a-lb-with-tf-xlb.jpeg)

## URL Maps in a GCP LB Created with Terraform
It is simple enough to copy/paste the required TF resources to create a GCP LB, but configuring the LB to route traffic in the way that you want isn't as straightforward. A URL map is used to send requests to the correct backend based on logic that you define.

### Host and Path Rules 
Creating rules based on the host and path of a request allows you to route traffic coming from specific points to specific backends.

 Host rules match the host name of a request, like "example.com". Each host rule has a path matcher rule that specifies the what path from that host should go to what backend. The most simple path mather rule is "/*" which matches all paths. 

 The **"google_compute_url_map"** resource accepts host and path matcher variables, for example: 
 
 ```
resource "google_compute_url_map" "urlmap" {
  name        = "my-urlmap"
  description = "Example url map"

  default_service = google_compute_backend_bucket.static.id

  host_rule {
    hosts        = ["example.com"]
    path_matcher = "example"
  }

  path_matcher {
    name            = "example"
    default_service = google_compute_backend_bucket.home.id

    path_rule {
      paths   = ["/home"]
      service = google_compute_backend_bucket.home.id
    }

    path_rule {
      paths   = ["/login"]
      service = google_compute_backend_service.login.id
    }

    path_rule {
      paths   = ["/static"]
      service = google_compute_backend_bucket.static.id
    }
  }
}
```
In the example you can see that the host rule will match requests for the host "example.com". That host rule references the path_matcher "example", which contains 3 path rules. Those path rules send traffic to a certain backend depending on what path the request is for. So a request for "example.com/home" will go to the backend google_compute_backend_bucket.home.

 In addition to host/path rules, the url map resource accepts many other arguments you may want to use for your load balancer. The Terraform registry includes a complete [list of arguments.](https://registry.terraform.io/providers/hashicorp/google/latest/docs/resources/compute_url_map#argument-reference)

 ## Example
 Below is a basic example of Terraform code that creates an external HTTPS load balancer in GCP that uses a NEG (network endpoint group) as a backend.
 ```
# Create network endpoint
resource "google_compute_global_network_endpoint" "default" {
  global_network_endpoint_group = google_compute_global_network_endpoint_group.default.name
  fqdn                          = "www.example.com"
  port                          = 90
}

# Add network endpoint to network endpoint group
resource "google_compute_global_network_endpoint_group" "default" {
  name                  = "example-neg"
  default_port          = "90"
  network_endpoint_type = "INTERNET_FQDN_PORT"
}

# Since this is an external LB it needs a SSL certificate
resource "google_compute_managed_ssl_certificate" "default" {
  name = "example-cert"

  managed {
    domains = ["example"]
  }
}

# Forwarding rule
resource "google_compute_global_forwarding_rule" "example" {
  name                  = "example-forwarding-rule"
  provider              = google-beta
  port_range            = "443"
  target                = google_compute_target_https_proxy.default.self_link
  ip_address            = google_compute_global_address.default.address
}

# Public IP address
resource "google_compute_global_address" "default" {
  provider      = google-beta
  name          = "example-address"
  ip_version    = "IPV4"
}

# HTTPS proxy 
resource "google_compute_target_https_proxy" "default" {
  name             = "example-proxy"
  url_map          = google_compute_url_map.default.id
  ssl_certificates = [google_compute_managed_ssl_certificate.default.id]
}

# URL Map
resource "google_compute_url_map" "default" {
  name        = "example-urlmap"
  description = "Example url map"

  default_service = google_compute_backend_service.default.id
  }

# Make NEG the backend
resource "google_compute_backend_service" "default" {
  name          = "example-backend-service"
  port_name     = "https"
  protocol      = "HTTPS"
  backend {
    group = google_compute_global_network_endpoint_group.default.self_link
    balancing_mode = "UTILIZATION"
    capacity_saler = 1.0
  }
}
 ```