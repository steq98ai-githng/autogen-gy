// Copyright (c) Microsoft Corporation. All rights reserved.
// ProtobufTypeNameResolver.cs

using System.Reflection;
using Google.Protobuf;
using Google.Protobuf.Reflection;

namespace Microsoft.AutoGen.Core.Grpc;

public class ProtobufTypeNameResolver : ITypeNameResolver
{
    public string ResolveTypeName(Type input)
    {
        if (typeof(IMessage).IsAssignableFrom(input))
        {
            var descriptorProperty = input.GetProperty("Descriptor", BindingFlags.Static | BindingFlags.Public);
            if (descriptorProperty != null)
            {
                if (descriptorProperty.GetValue(null) is MessageDescriptor descriptor)
                {
                    return descriptor.FullName;
                }
            }

            var protoMessage = (IMessage?)Activator.CreateInstance(input) ?? throw new InvalidOperationException($"Failed to create instance of {input.FullName}");
            return protoMessage.Descriptor.FullName;
        }
        else
        {
            throw new ArgumentException("Input must be a protobuf message.");
        }
    }
}
