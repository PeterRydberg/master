"""
This type stub file was generated by pyright.
"""

class Session(object):
    """
    A session stores configuration state and allows you to create service
    clients and resources.

    :type aws_access_key_id: string
    :param aws_access_key_id: AWS access key ID
    :type aws_secret_access_key: string
    :param aws_secret_access_key: AWS secret access key
    :type aws_session_token: string
    :param aws_session_token: AWS temporary session token
    :type region_name: string
    :param region_name: Default region when creating new connections
    :type botocore_session: botocore.session.Session
    :param botocore_session: Use this Botocore session instead of creating
                             a new default one.
    :type profile_name: string
    :param profile_name: The name of a profile to use. If not given, then
                         the default profile is used.
    """
    def __init__(self, aws_access_key_id=..., aws_secret_access_key=..., aws_session_token=..., region_name=..., botocore_session=..., profile_name=...) -> None:
        ...
    
    def __repr__(self):
        ...
    
    @property
    def profile_name(self):
        """
        The **read-only** profile name.
        """
        ...
    
    @property
    def region_name(self):
        """
        The **read-only** region name.
        """
        ...
    
    @property
    def events(self):
        """
        The event emitter for a session
        """
        ...
    
    @property
    def available_profiles(self):
        """
        The profiles available to the session credentials
        """
        ...
    
    def get_available_services(self):
        """
        Get a list of available services that can be loaded as low-level
        clients via :py:meth:`Session.client`.

        :rtype: list
        :return: List of service names
        """
        ...
    
    def get_available_resources(self):
        """
        Get a list of available services that can be loaded as resource
        clients via :py:meth:`Session.resource`.

        :rtype: list
        :return: List of service names
        """
        ...
    
    def get_available_partitions(self):
        """Lists the available partitions

        :rtype: list
        :return: Returns a list of partition names (e.g., ["aws", "aws-cn"])
        """
        ...
    
    def get_available_regions(self, service_name, partition_name=..., allow_non_regional=...):
        """Lists the region and endpoint names of a particular partition.

        :type service_name: string
        :param service_name: Name of a service to list endpoint for (e.g., s3).

        :type partition_name: string
        :param partition_name: Name of the partition to limit endpoints to.
            (e.g., aws for the public AWS endpoints, aws-cn for AWS China
            endpoints, aws-us-gov for AWS GovCloud (US) Endpoints, etc.)

        :type allow_non_regional: bool
        :param allow_non_regional: Set to True to include endpoints that are
             not regional endpoints (e.g., s3-external-1,
             fips-us-gov-west-1, etc).

        :return: Returns a list of endpoint names (e.g., ["us-east-1"]).
        """
        ...
    
    def get_credentials(self):
        """
        Return the :class:`botocore.credential.Credential` object
        associated with this session.  If the credentials have not
        yet been loaded, this will attempt to load them.  If they
        have already been loaded, this will return the cached
        credentials.
        """
        ...
    
    def client(self, service_name, region_name=..., api_version=..., use_ssl=..., verify=..., endpoint_url=..., aws_access_key_id=..., aws_secret_access_key=..., aws_session_token=..., config=...):
        """
        Create a low-level service client by name.

        :type service_name: string
        :param service_name: The name of a service, e.g. 's3' or 'ec2'. You
            can get a list of available services via
            :py:meth:`get_available_services`.

        :type region_name: string
        :param region_name: The name of the region associated with the client.
            A client is associated with a single region.

        :type api_version: string
        :param api_version: The API version to use.  By default, botocore will
            use the latest API version when creating a client.  You only need
            to specify this parameter if you want to use a previous API version
            of the client.

        :type use_ssl: boolean
        :param use_ssl: Whether or not to use SSL.  By default, SSL is used.
            Note that not all services support non-ssl connections.

        :type verify: boolean/string
        :param verify: Whether or not to verify SSL certificates.  By default
            SSL certificates are verified.  You can provide the following
            values:

            * False - do not validate SSL certificates.  SSL will still be
              used (unless use_ssl is False), but SSL certificates
              will not be verified.
            * path/to/cert/bundle.pem - A filename of the CA cert bundle to
              uses.  You can specify this argument if you want to use a
              different CA cert bundle than the one used by botocore.

        :type endpoint_url: string
        :param endpoint_url: The complete URL to use for the constructed
            client. Normally, botocore will automatically construct the
            appropriate URL to use when communicating with a service.  You
            can specify a complete URL (including the "http/https" scheme)
            to override this behavior.  If this value is provided,
            then ``use_ssl`` is ignored.

        :type aws_access_key_id: string
        :param aws_access_key_id: The access key to use when creating
            the client.  This is entirely optional, and if not provided,
            the credentials configured for the session will automatically
            be used.  You only need to provide this argument if you want
            to override the credentials used for this specific client.

        :type aws_secret_access_key: string
        :param aws_secret_access_key: The secret key to use when creating
            the client.  Same semantics as aws_access_key_id above.

        :type aws_session_token: string
        :param aws_session_token: The session token to use when creating
            the client.  Same semantics as aws_access_key_id above.

        :type config: botocore.client.Config
        :param config: Advanced client configuration options. If region_name
            is specified in the client config, its value will take precedence
            over environment variables and configuration values, but not over
            a region_name value passed explicitly to the method. See
            `botocore config documentation
            <https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html>`_
            for more details.

        :return: Service client instance

        """
        ...
    
    def resource(self, service_name, region_name=..., api_version=..., use_ssl=..., verify=..., endpoint_url=..., aws_access_key_id=..., aws_secret_access_key=..., aws_session_token=..., config=...):
        """
        Create a resource service client by name.

        :type service_name: string
        :param service_name: The name of a service, e.g. 's3' or 'ec2'. You
            can get a list of available services via
            :py:meth:`get_available_resources`.

        :type region_name: string
        :param region_name: The name of the region associated with the client.
            A client is associated with a single region.

        :type api_version: string
        :param api_version: The API version to use.  By default, botocore will
            use the latest API version when creating a client.  You only need
            to specify this parameter if you want to use a previous API version
            of the client.

        :type use_ssl: boolean
        :param use_ssl: Whether or not to use SSL.  By default, SSL is used.
            Note that not all services support non-ssl connections.

        :type verify: boolean/string
        :param verify: Whether or not to verify SSL certificates.  By default
            SSL certificates are verified.  You can provide the following
            values:

            * False - do not validate SSL certificates.  SSL will still be
              used (unless use_ssl is False), but SSL certificates
              will not be verified.
            * path/to/cert/bundle.pem - A filename of the CA cert bundle to
              uses.  You can specify this argument if you want to use a
              different CA cert bundle than the one used by botocore.

        :type endpoint_url: string
        :param endpoint_url: The complete URL to use for the constructed
            client. Normally, botocore will automatically construct the
            appropriate URL to use when communicating with a service.  You
            can specify a complete URL (including the "http/https" scheme)
            to override this behavior.  If this value is provided,
            then ``use_ssl`` is ignored.

        :type aws_access_key_id: string
        :param aws_access_key_id: The access key to use when creating
            the client.  This is entirely optional, and if not provided,
            the credentials configured for the session will automatically
            be used.  You only need to provide this argument if you want
            to override the credentials used for this specific client.

        :type aws_secret_access_key: string
        :param aws_secret_access_key: The secret key to use when creating
            the client.  Same semantics as aws_access_key_id above.

        :type aws_session_token: string
        :param aws_session_token: The session token to use when creating
            the client.  Same semantics as aws_access_key_id above.

        :type config: botocore.client.Config
        :param config: Advanced client configuration options. If region_name
            is specified in the client config, its value will take precedence
            over environment variables and configuration values, but not over
            a region_name value passed explicitly to the method.  If
            user_agent_extra is specified in the client config, it overrides
            the default user_agent_extra provided by the resource API. See
            `botocore config documentation
            <https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html>`_
            for more details.

        :return: Subclass of :py:class:`~boto3.resources.base.ServiceResource`
        """
        ...
    


