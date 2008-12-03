class SOAP:

	WSDL = '''
		<?xml version="1.0" encoding="utf-8"?>
		<wsdl:definitions
			xmlns:s="http://www.w3.org/2001/XMLSchema"
			xmlns:soap12="http://schemas.xmlsoap.org/wsdl/soap12/"
			xmlns:mime="http://schemas.xmlsoap.org/wsdl/mime/"
			xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
			xmlns:http="http://schemas.xmlsoap.org/wsdl/http/"
			xmlns:soapenc="http://schemas.xmlsoap.org/soap/encoding/"
			xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/"

			xmlns:tns="{{namespace}}"
			targetNamespace="{{namespace}}" >

			<wsdl:types>
				<s:schema elementFormDefault="qualified" targetNamespace="{{namespace}}">
					{{for method in methods }}
					<s:element name="{{method['name']}}">
						<s:complexType>
							<s:sequence>
								{{for argument in method['arguments']}}
								<s:element minOccurs="1" maxOccurs="1" name="{{argument['name']}}"
									type="s:{{argument['type']}}" />
								{{endfor}}
							</s:sequence>
						</s:complexType>
					</s:element>
					<s:element name="{{method['name']}}Response">
						<s:complexType>
							<s:sequence>
								<s:element minOccurs="1" maxOccurs="1" name="{{method['name']}}Result" type="s:{{method['returntype']}}" />
							</s:sequence>
						</s:complexType>
					</s:element>
					
					{{endfor}}
				</s:schema>
			</wsdl:types>
			
			{{for method in methods }}
			<wsdl:message name="{{method['name']}}SoapIn">
				<wsdl:part name="parameters" element="tns:{{method['name']}}" />

			</wsdl:message>
			<wsdl:message name="{{method['name']}}SoapOut">
				<wsdl:part name="parameters" element="tns:{{method['name']}}Response" />
			</wsdl:message>
			{{endfor}}

			<wsdl:portType name="{{appname}}Soap">
				{{for method in methods }}
				<wsdl:operation name="{{method['name']}}">
					<wsdl:input message="tns:{{method['name']}}SoapIn" />
					<wsdl:output message="tns:{{method['name']}}SoapOut" />
				</wsdl:operation>
				{{endfor}}
			</wsdl:portType>

			<wsdl:binding name="{{appname}}Soap" type="tns:{{appname}}Soap">
				<soap:binding transport="http://schemas.xmlsoap.org/soap/http" />

				{{for method in methods }}
				<wsdl:operation name="{{method['name']}}">
					<soap:operation soapAction="{{namespace}}/{{appname}}/{{method['name']}}" style="document" />
					<wsdl:input>
						<soap:body use="literal" />
					</wsdl:input>

					<wsdl:output>
						<soap:body use="literal" />
					</wsdl:output>
				</wsdl:operation>
				{{endfor}}
			</wsdl:binding>

			<wsdl:binding name="{{appname}}Soap12" type="tns:{{appname}}Soap">
				<soap12:binding transport="http://schemas.xmlsoap.org/soap/http" />

				{{for method in methods }}
				<wsdl:operation name="{{method['name']}}">
					<soap12:operation soapAction="{{namespace}}/{{appname}}/{{method['name']}}" style="document" />
					<wsdl:input>
						<soap12:body use="literal" />
					</wsdl:input>

					<wsdl:output>
						<soap12:body use="literal" />
					</wsdl:output>
				</wsdl:operation>
				{{endfor}}
			</wsdl:binding>

			<wsdl:service name="{{appname}}">

				<wsdl:port name="{{appname}}Soap" binding="tns:{{appname}}Soap">
					<soap:address location="{{namespace}}/{{appname}}" />
				</wsdl:port>
				<wsdl:port name="{{appname}}Soap12" binding="tns:{{appname}}Soap12">
					<soap12:address location="{{namespace}}/{{appname}}" />
				</wsdl:port>
			</wsdl:service>

		</wsdl:definitions>
	'''

	Response = '''
		<?xml version="1.0" encoding="utf-8"?>
		<soap:Envelope
			xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
			xmlns:xsd="http://www.w3.org/2001/XMLSchema"
			xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" >

		  <soap:Body>
			<{{method['name']}}Response xmlns="{{namespace}}">
			  <{{method['name']}}Result>{{method['response']}}</{{method['name']}}Result>
			</{{method['name']}}Response>
		  </soap:Body>
		</soap:Envelope>
	'''
