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
            // Try to get the descriptor from the static property first to avoid instantiation
            var descriptor = input.GetProperty("Descriptor", BindingFlags.Static | BindingFlags.Public)?.GetValue(null) as MessageDescriptor;
            if (descriptor != null)
            {
                return descriptor.FullName;
            }

            // Fallback to instantiation if static property is not found
            var protoMessage = (IMessage?)Activator.CreateInstance(input) ?? throw new InvalidOperationException($"Failed to create instance of {input.FullName}");
            return protoMessage.Descriptor.FullName;
        }
        else
        {
            throw new ArgumentException("Input must be a protobuf message.");
        }
    }
}
